#! /usr/bin/env python

# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org> This program is free
# software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import numpy as np
import h5py

from time import time
import os
import warnings

import pesummary
from pesummary.utils.utils import logger
from pesummary.gw.file.read import read as GWRead
from pesummary.core.inputs import Input
from pesummary.utils.utils import customwarn

warnings.showwarning = customwarn

__doc__ == "Classes to handle the command line inputs"


class GWInput(Input):
    """Super class to handle command line arguments

    Parameters
    ----------
    parser: argparser
        The parser containing the command line arguments

    Attributes
    ----------
    user: str
        The user who submitted the job
    add_to_existing: Bool
        Boolean to determine if you wish to add to a existing webpage
    existing: str
        Existing web directory
    webdir: str
        Directory to output all information
    baseurl: str
        The url path for the corresponding web directory
    inj_file: List
        List containing paths to the injection file
    result_files: list
        List containing paths to the results files which are being analysed
    config: list
        List containing paths to the configuration files used to generate each
        results files
    approximant: list
        List of approximants used in the analysis to generate each results
        files
    email: str
        The email address to notify when the job has completed
    sensitivity: Bool
        Boolean to determine if you wish to plot the sky sensitivity for
        different detector networks
    gracedb: str
        The gracedb of the event that produced the results files
    dump: Bool
        Boolean to determine if you wish to produce a dumped html page layout
    detectors: list
        List containing the detectors used to generate each results file
    labels: str
        A label for this summary page
    psd: str
        List of the psds used in the analysis
    """
    def __init__(self, opts):
        logger.info("Command line arguments: %s" % (opts))
        self.opts = opts
        self.user = self.opts.user
        self.existing = self.opts.existing
        self.webdir = self.opts.webdir
        self.publication = self.opts.publication
        self.kde_plot = self.opts.kde_plot
        self.make_directories()
        self.baseurl = self.opts.baseurl
        self.inj_file = self.opts.inj_file
        self.config = self.opts.config
        self.compare_results = self.opts.compare_results
        self.result_files = self.opts.samples
        self.custom_plotting = self.opts.custom_plotting
        self.email = self.opts.email
        self.add_to_existing = self.opts.add_to_existing
        self.dump = self.opts.dump
        self.hdf5 = opts.save_to_hdf5
        self.gracedb = self.opts.gracedb
        self.detectors = None
        self.calibration = self.opts.calibration
        self.approximant = self.opts.approximant
        self.sensitivity = self.opts.sensitivity
        self.no_ligo_skymap = self.opts.no_ligo_skymap
        self.multi_threading_for_skymap = self.opts.multi_threading_for_skymap
        self.nsamples_for_skymap = self.opts.nsamples_for_skymap
        self.psds = self.opts.psd
        self.gwdata = self.opts.gwdata
        self.existing_labels = []
        self.existing_version = []
        self.existing_metadata = []
        self.existing_parameters = []
        self.existing_samples = []
        self.existing_approximant = []
        self.labels = self.opts.labels
        self.copy_files()

    @property
    def approximant(self):
        return self._approximant

    @approximant.setter
    def approximant(self, approximant):
        approximant_list = [None] * len(self.result_files)
        if not approximant:
            logger.warning("No approximant given. Waveform plots will not be "
                           "generated")
        else:
            approximant_list = approximant
        if approximant_list and len(approximant_list) != len(self.result_files):
            raise Exception("The number of results files does not match the "
                            "number of approximants")
        self._approximant = approximant_list

    @property
    def gracedb(self):
        return self._gracedb

    @gracedb.setter
    def gracedb(self, gracedb):
        self._gracedb = None
        if gracedb:
            self._gracedb = gracedb

    @property
    def detectors(self):
        return self._detectors

    @detectors.setter
    def detectors(self, detectors):
        detector_list = []
        if not detectors:
            for num, i in enumerate(self.result_files):
                params = self.parameters[num]
                individual_detectors = []
                for j in params:
                    if "optimal_snr" in j and j != "network_optimal_snr":
                        det = j.split("_optimal_snr")[0]
                        individual_detectors.append(det)
                individual_detectors = sorted(
                    [str(i) for i in individual_detectors])
                if individual_detectors:
                    detector_list.append("_".join(individual_detectors))
                else:
                    detector_list.append(None)
        else:
            detector_list = detectors
        logger.debug("The detector network is %s" % (detector_list))
        self._detectors = detector_list

    @property
    def psds(self):
        return self._psds

    @psds.setter
    def psds(self, psds):
        psd_list = []
        if psds:
            if isinstance(psds, dict):
                keys = psds.keys()
                for key in keys:
                    if isinstance(psds[key], str):
                        self._check_psd_extension(psds[key])
                    else:
                        for j in psds[key]:
                            self._check_psd_extension(j)
                psd_list = psds
            else:
                for i in psds:
                    self._check_psd_extension(i)
                    psd_list.append(i)
            self._psds = psd_list
        else:
            self._psds = None

    @property
    def gwdata(self):
        return self._gwdata

    @gwdata.setter
    def gwdata(self, gwdata):
        from pesummary.gw.file.formats.base_read import GWRead as StrainFile
        self._gwdata = None
        if gwdata:
            for i in gwdata.keys():
                if not os.path.isfile(gwdata[i]):
                    raise Exception("The file %s does not exist. Please check "
                                    "the path to your strain file")
            timeseries = StrainFile.load_strain_data(gwdata)
            self._gwdata = timeseries

    @property
    def nsamples_for_skymap(self):
        return self._nsamples_for_skymap

    @nsamples_for_skymap.setter
    def nsamples_for_skymap(self, nsamples_for_skymap):
        self._nsamples_for_skymap = nsamples_for_skymap
        if nsamples_for_skymap:
            self._nsamples_for_skymap = int(nsamples_for_skymap)

    def _check_psd_extension(self, file):
        """Check that the file extension on the psd file can be read and
        understood by PESummary.

        Parameters
        ----------
        file: str
            path to the file that you would like to check
        """
        extension = file.split(".")[-1]
        if extension == "gz":
            print("convert to .dat file")
        elif extension == "dat":
            pass
        elif extension == "txt":
            pass
        else:
            raise Exception("PSD results file not understood")

    @property
    def calibration(self):
        return self._calibration

    @calibration.setter
    def calibration(self, calibration):
        calibration_list = []
        if calibration:
            if isinstance(calibration, dict):
                calibration_list = calibration
            else:
                for i in calibration:
                    calibration_list.append(i)
            self._calibration = calibration_list
        else:
            label_list, data_list = [], []
            for i in self.result_files:
                f = GWRead(i)
                calib_data = f.calibration_data_in_results_file
                if calib_data is None:
                    data_list.append(None)
                    label_list.append(None)
                elif isinstance(f, pesummary.gw.file.formats.pesummary.PESummary):
                    for num, i in enumerate(calib_data[0]):
                        data_list.append(i)
                        label_list.append(list(calib_data[1][num]))
                else:
                    data_list.append(calib_data[0])
                    label_list.append(list(calib_data[1]))
            calibration_list = data_list
            self._calibration = calibration_list
            self.calibration_envelopes = calibration_list
            self.calibration_labels = label_list

    def _check_calibration_file(self, file):
        """Check the contents of the calibration file to ensure that it is
        of the correct format.

        Parameters
        ----------
        file: str
            path to the calibration file
        """
        try:
            f = np.genfromtxt(file)
            if len(f[0]) != 7:
                raise Exception("Calibration envelope file not understood")
            pass
        except Exception:
            pass

    @staticmethod
    def grab_data_from_metafile(existing_file, webdir="./", compare=None):
        """Grab the data from a metafile

        Parameters
        ----------
        existing_file: str
            path to the existing PESummary metafile
        webdir: str
            path to the web directory
        compare: list
            list of labels for the events that you wish to compare
        """
        f = GWRead(existing_file)
        labels = f.labels
        indicies = [i for i in range(len(labels))]

        if compare:
            for i in compare:
                if i not in labels:
                    raise Exception("Label %s does not exist in the metafile. "
                                    "Please check that the labels for the runs "
                                    "you wish to compare are correct." % (i))
            indicies = [labels.index(i) for i in compare]

        p = [f.parameters[i] for i in indicies]
        s = [f.samples[i] for i in indicies]

        if f.injection_parameters == []:
            inj_values = []
        else:
            inj_values = [f.injection_parameters[i] for i in indicies]

        if inj_values == []:
            for num, i in enumerate(p):
                inj_values.append([float("nan")] * len(i))

        approximant = [f.approximant[i] for i in indicies]
        label = lambda i: f.labels[i]

        if f.config is not None:
            config = []
            for i in indicies:
                f.write_config_to_file(label(i), outdir="%s/config" % (webdir))
                config.append("%s/config/%s_config.ini" % (webdir, label(i)))
        else:
            config = None

        if f.psd is not None and f.psd[label(indicies[0])] != {}:
            psd = ["extracted_%s.txt" % (f.psd[label(i)]) for i in indicies]

            psd_labels = [[i for i in list(f.psd[label(idx)].keys())]
                          for idx in indicies]

            psd_frequencies = [[[l[0] for l in f.psd[label(idx)][k]]
                               for k in f.psd[label(idx)].keys()]
                               for idx in indicies]

            psd_strains = [[[l[1] for l in f.psd[label(idx)][k]]
                           for k in f.psd[label(idx)].keys()]
                           for idx in indicies]
        else:
            psd = psd_labels = psd_frequencies = psd_strains = None

        if f.calibration is not None and f.calibration[label(indicies[0])] != {}:
            calibration, calibration_labels, calibration_envelopes = [], [], []
            for i in indicies:
                if label(i) in list(f.calibration.keys()):
                    calibration.append("extracted_%s.txt" % (
                        f.calibration[label(i)]))
                    calibration_labels.append([
                        i for i in list(f.calibration[label(i)])])
                    calibration_envelopes.append(np.array([
                        f.calibration[label(i)][k] for k in
                        f.calibration[label(i)].keys()]))
                else:
                    calibration.append(None)
                    calibration_labels.append(None)
                    calibration_envelopes.append(None)
        else:
            calibration = calibration_labels = calibration_envelopes = None
        labels = [labels[i] for i in indicies]
        version = f.input_version
        meta_data = f.extra_kwargs
        return p, s, inj_values, labels, psd, approximant, psd_labels, \
            psd_frequencies, psd_strains, calibration, calibration_labels, \
            calibration_envelopes, config, version, meta_data

    def grab_data_from_input_files(self, samples):
        """
        """
        result_file_list, version_list, kwarg_list = [], [], []
        parameters_list, samples_list, injection_list = [], [], []
        psd_labels, psd_frequencies, psd_strains = [], [], []
        calibration_labels, calibration_envelopes = [], []
        for num, i in enumerate(samples):
            if not os.path.isfile(i):
                raise Exception("File %s does not exist" % (i))
            config = None
            if self.config:
                config = self.config[num]
            if self.is_pesummary_metafile(i):
                p, s, inj, labels, psd, approx, psd_l, psd_f, psd_s, cal, cal_l, cal_env, con, ver, md = \
                    self.grab_data_from_metafile(
                        i, webdir=self.webdir, compare=self.compare_results)
                self.opts.psd = psd
                self.opts.calibration = cal
                self.opts.labels = labels
                self.opts.approximant = approx
                self.config = con
                for idx, j in enumerate(p):
                    parameters_list.append(j)
                    samples_list.append(s[idx])
                    injection_list.append(inj[idx])
                    result_file_list.append(i)
                    version_list.append(ver[idx])
                    kwarg_list.append(md[idx])
                    if psd is not None:
                        psd_labels.append(psd_l[idx])
                        psd_frequencies.append(psd_f[idx])
                        psd_strains.append(psd_s[idx])
                    if cal is not None:
                        calibration_labels.append(cal_l[idx])
                        calibration_envelopes.append(cal_env[idx])
            else:
                p, s, inj, version, kwargs = self.convert_to_standard_format(
                    i, self.inj_file[num], config_file=config)
                result_file_list.append(i)
                parameters_list.append(p)
                samples_list.append(s)
                injection_list.append(inj)
                version_list.append(version)
                kwarg_list.append(kwargs)
        self._result_files = result_file_list
        self._parameters = parameters_list
        self._samples = samples_list
        self._injection_data = injection_list
        self._file_versions = version_list
        self._file_kwargs = kwarg_list

        if psd_labels != [] and psd_frequencies != [] and psd_strains != []:
            self.psd_labels = psd_labels
            self.psd_frequencies = psd_frequencies
            self.psd_strains = psd_strains

        if calibration_labels != [] and calibration_envelopes != []:
            self.calibration_labels = calibration_labels
            self.calibration_envelopes = calibration_envelopes

    @property
    def existing_approximant(self):
        return self._existing_approximant

    @existing_approximant.setter
    def existing_approximant(self, existing_approximant):
        self._existing_approximant = None
        if self.add_to_existing:
            existing = GWRead(self.existing_meta_file)
            self._existing_approximant = existing.approximant

    @staticmethod
    def _IFO_from_file_name(file):
        """Return a guess of the IFO from the file name.

        Parameters
        ----------
        file: str
            the name of the file that you would like to make a guess for
        """
        file_name = file.split("/")[-1]
        if any(j in file_name for j in ["H1", "_0", "IFO0"]):
            ifo = "H1"
        elif any(j in file_name for j in ["L1", "_1", "IFO1"]):
            ifo = "L1"
        elif any(j in file_name for j in ["V1", "_2", "IFO2"]):
            ifo = "V1"
        else:
            ifo = file_name
        return ifo

    def convert_to_standard_format(self, results_file, injection_file=None,
                                   config_file=None):
        """Convert a results file to standard form.

        Parameters
        ----------
        results_file: str
            Path to the results file that you wish to convert to standard
            form
        injection_file: str, optional
            Path to the injection file that was used in the analysis to
            produce the results_file
        config_file: str, optional
            Path to the configuration file that was used
        """
        f = GWRead(results_file)
        if config_file:
            f.add_fixed_parameters_from_config_file(config_file)
            f.add_marginalized_parameters_from_config_file(config_file)
        f.generate_all_posterior_samples()
        parameters = f.parameters
        samples = f.samples
        extra_kwargs = f.extra_kwargs
        if injection_file:
            f.add_injection_parameters_from_file(injection_file)
        if hasattr(f, "injection_parameters"):
            injection = f.injection_parameters
            if injection is not None:
                for i in parameters:
                    if i not in list(injection.keys()):
                        injection[i] = float("nan")
            else:
                injection = {i: j for i, j in zip(
                    parameters, [float("nan")] * len(parameters))}
        else:
            injection = {i: j for i, j in zip(
                parameters, [float("nan")] * len(parameters))}
        version = f.input_version
        return parameters, samples, injection, version, extra_kwargs

    def _default_labels(self):
        """Return the defaut labels given your detector network.
        """
        label_list = []
        for num, i in enumerate(self.result_files):
            if self.gracedb and self.detectors[num]:
                label_list.append("_".join(
                    [self.gracedb, self.detectors[num]]))
            elif self.gracedb:
                label_list.append(self.gracedb)
            elif self.detectors[num]:
                label_list.append(self.detectors[num])
            else:
                file_name = ".".join(i.split("/")[-1].split(".")[:-1])
                label_list.append("%s_%s" % (round(time()), file_name))

        duplicates = dict(set(
            (x, label_list.count(x)) for x in
            filter(lambda rec: label_list.count(rec) > 1, label_list)))
        for i in duplicates.keys():
            for j in range(duplicates[i]):
                ind = label_list.index(i)
                label_list[ind] += "_%s" % (j)
        if self.add_to_existing:
            for num, i in enumerate(label_list):
                if i in self.existing_labels:
                    ind = label_list.index(i)
                    label_list[ind] += "_%s" % (num)
        return label_list


class GWPostProcessing(pesummary.core.inputs.PostProcessing):
    """Class to extract parameters from the results files

    Parameters
    ----------
    inputs: argparser
        The parser containing the command line arguments
    colors: list, optional
        colors that you would like to use to display each results file in the
        webpage

    Attributes
    ----------
    parameters: list
        list of parameters that have posterior distributions for each results
        file
    injection_data: list
        list of dictionaries that contain the injection parameters and their
        injected value for each results file
    samples: list
        list of posterior samples for each parameter for each results file
    maxL_samples: list
        list of dictionaries that contain each parameter and their
        corresponding maximum likelihood value for each results file
    same_parameters: list
        List of parameters that all results files have sampled over
    """
    def __init__(self, inputs, colors="default"):
        self.inputs = inputs
        self.webdir = inputs.webdir
        self.baseurl = inputs.baseurl
        self.result_files = inputs.result_files
        self.custom_plotting = inputs.custom_plotting
        self.dump = inputs.dump
        self.email = inputs.email
        self.user = inputs.user
        self.host = inputs.host
        self.config = inputs.config
        self.existing = inputs.existing
        self.add_to_existing = inputs.add_to_existing
        self.labels = inputs.labels
        self.hdf5 = inputs.hdf5
        self.publication = inputs.publication
        self.kde_plot = inputs.kde_plot
        self.existing_meta_file = inputs.existing_meta_file
        self.existing_labels = inputs.existing_labels
        self.existing_version = inputs.existing_version
        self.existing_metadata = inputs.existing_metadata
        self.existing_parameters = inputs.existing_parameters
        self.existing_samples = inputs.existing_samples
        self.existing_meta_file = inputs.existing_meta_file
        self.colors = colors
        self.approximant = inputs.approximant
        self.detectors = inputs.detectors
        self.gracedb = inputs.gracedb
        self.calibration = inputs.calibration
        self.calibration_labels = None
        self.sensitivity = inputs.sensitivity
        self.psds = inputs.psds
        self.gwdata = inputs.gwdata
        self.psd_dict = False
        self.psd_list = False
        if isinstance(self.psds, dict):
            self.psd_dict = True
        else:
            self.psd_list = True
        self.calibration_dict = False
        self.calibration_list = False
        if isinstance(self.calibration, dict):
            self.calibration_dict = True
        else:
            self.calibration_list = True
        self.no_ligo_skymap = inputs.no_ligo_skymap
        self.multi_threading_for_skymap = inputs.multi_threading_for_skymap
        self.nsamples_for_skymap = inputs.nsamples_for_skymap

        self.grab_data_map = {"existing_file": self._data_from_existing_file,
                              "standard_format": self._data_from_standard_format}

        self.parameters = inputs.parameters
        self.samples = inputs.samples
        self.injection_data = inputs.injection_data
        self.file_versions = inputs.file_versions
        self.file_kwargs = inputs.file_kwargs
        self.maxL_samples = []
        self.same_parameters = []
        self.pepredicates_probs = []

    @property
    def coherence_test(self):
        return False

    @property
    def maxL_samples(self):
        return self._maxL_samples

    @maxL_samples.setter
    def maxL_samples(self, maxL_samples):
        key_data = self._key_data()
        maxL_list = []
        for num, i in enumerate(self.parameters):
            dictionary = {j: key_data[num][j]["maxL"] for j in i}
            if self.approximant:
                dictionary["approximant"] = self.approximant[num]
            maxL_list.append(dictionary)
        self._maxL_samples = maxL_list

    @property
    def label_to_prepend_approximant(self):
        labels = [i[len(self.gracedb) + 1:] if self.gracedb else i for i in
                  self.labels]
        prepend = [None] * len(self.approximant)
        duplicates = dict(set(
            (x, self.approximant.count(x)) for x in filter(
                lambda rec: self.approximant.count(rec) > 1,
                self.approximant)))
        if len(duplicates.keys()) > 0:
            for num, i in enumerate(self.approximant):
                if i in duplicates.keys():
                    prepend[num] = labels[num]
        return prepend

    @property
    def psd_labels(self):
        if hasattr(self.inputs, "psd_labels"):
            return self.inputs.psd_labels
        elif self.psds:
            return self._labels_from_dictionary(self.psds)
        return None

    @property
    def calibration_labels(self):
        return self._calibration_labels

    @calibration_labels.setter
    def calibration_labels(self, calibration_labels):
        if hasattr(self.inputs, "calibration_labels"):
            self._calibration_labels = self.inputs.calibration_labels
        elif not calibration_labels and self.calibration:
            self._calibration_labels = self._labels_from_dictionary(
                self.calibration)
        elif self.calibration:
            self._calibration_labels = calibration_labels
        else:
            self._calibration_labels = None

    @property
    def psd_frequencies(self):
        if hasattr(self.inputs, "psd_frequencies"):
            return self.inputs.psd_frequencies
        return self._setup_psd_calibration(
            self.psds, self.psd_labels,
            self._grab_frequencies_from_psd_data_file)

    @property
    def psd_strains(self):
        if hasattr(self.inputs, "psd_strains"):
            return self.inputs.psd_strains
        return self._setup_psd_calibration(
            self.psds, self.psd_labels,
            self._grab_strains_from_psd_data_file)

    @property
    def calibration_envelopes(self):
        if hasattr(self.inputs, "calibration_envelopes"):
            return self.inputs.calibration_envelopes
        try:
            return self._setup_psd_calibration(
                self.calibration, self.calibration_labels,
                self._grab_calibration_data_from_data_file)
        except Exception:
            raise Exception("Failed to extract data from calibration files")

    @staticmethod
    def _IFO_from_file_name(file):
        """Return a guess of the IFO from the file name.

        Parameters
        ----------
        file: str
            the name of the file that you would like to make a guess for
        """
        file_name = file.split("/")[-1]
        if any(j in file_name for j in ["H1", "_0", "IFO0"]):
            ifo = "H1"
        elif any(j in file_name for j in ["L1", "_1", "IFO1"]):
            ifo = "L1"
        elif any(j in file_name for j in ["V1", "_2", "IFO2"]):
            ifo = "V1"
        else:
            ifo = file_name
        return ifo

    def _setup_psd_calibration(self, data, labels, executable):
        """Determine which result files correspond to which calibration/psd
        files.

        Parameters
        ----------
        data: list/dict
            list/dict containing paths to calibration/psd files
        labels: list
            list of labels corresponding to the calibration/psd files
        executable: PESummary object
            executable that is used to extract the data from the calibration/psd
            files
        """
        output = []
        if not isinstance(data, dict):
            for i in labels:
                temp = [executable(i) for i in data]
                output.append(temp)
        else:
            keys = list(data.keys())
            if isinstance(data[keys[0]], list):
                for idx in range(len(data[keys[0]])):
                    temp = [executable(data[i][idx]) for i in list(keys)]
                    output.append(temp)
            else:
                for i in labels:
                    temp = [executable(data[i]) for i in list(keys)]
                    output.append(temp)
        return output

    def _labels_from_dictionary(self, input):
        """Return the labels from either a list of a dictionary input

        Parameters
        ----------
        input: list/dict
            list/dict containing paths to files
        """
        if isinstance(input, dict):
            keys = list(input.keys())
            if isinstance(input[keys[0]], list):
                return [[i for i in input.keys()] for j in range(len(self.labels))]
            else:
                return [[i for i in input.keys()] for j in input]
        return [[self._IFO_from_file_name(i) for i in input] for j in
                range(len(self.labels))]

    def _key_data(self):
        """Grab the mean, median, maximum likelihood value and the standard
        deviation of each posteiror distribution for each results file.
        """
        key_data_list = []
        for num, i in enumerate(self.samples):
            data = {}
            likelihood_ind = self.parameters[num].index("log_likelihood")
            logL = [j[likelihood_ind] for j in i]
            for ind, j in enumerate(self.parameters[num]):
                index = self.parameters[num].index("%s" % (j))
                subset = [k[index] for k in i]
                data[j] = {"mean": np.mean(subset),
                           "median": np.median(subset),
                           "std": np.std(subset)}
                if np.max(logL) == 0:
                    data[j]["maxL"] = float("nan")
                else:
                    data[j]["maxL"] = subset[logL.index(np.max(logL))]
            key_data_list.append(data)
        return key_data_list

    def _grab_frequencies_from_psd_data_file(self, file):
        """Return the frequencies stored in the psd data files

        Parameters
        ----------
        file: str
            path to the psd data file
        """
        fil = np.genfromtxt(file, skip_footer=1)
        frequencies = fil.T[0].tolist()
        return frequencies

    def _grab_strains_from_psd_data_file(self, file):
        """Return the strains stored in the psd data files

        Parameters
        ----------
        file: str
            path to the psd data file
        """
        fil = np.genfromtxt(file, skip_footer=1)
        strains = fil.T[1].tolist()
        return strains

    def _grab_calibration_data_from_data_file(self, file):
        """Return the data stored in the calibration data file

        Parameters
        ----------
        file: str
            path to the calibration data file
        """
        try:
            f = np.genfromtxt(file)
            return f
        except Exception:
            return file

    @property
    def pepredicates_probs(self):
        return self._pepredicates_probs

    @pepredicates_probs.setter
    def pepredicates_probs(self, pepredicates_probs):
        classifications = []

        for num, i in enumerate(self.result_files):
            mydict = {}
            try:
                from pesummary.gw.pepredicates import PEPredicates
                from pesummary.utils.utils import RedirectLogger

                with RedirectLogger("PEPredicates", level="DEBUG") as redirector:
                    mydict["default"], mydict["population"] = \
                        PEPredicates.classifications(
                            self.samples[num], self.parameters[num])
            except Exception as e:
                logger.warn(
                    "Failed to generate source classification probabilities "
                    "for %s because of %s" % (i, e))
                mydict["default"] = None
                mydict["population"] = None
            classifications.append(mydict)
        self._pepredicates_probs = classifications
