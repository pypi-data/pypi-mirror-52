#!/usr/bin/env python
"""
bilby_pipe is a command line tools for taking user input (as command line
arguments or an ini file) and creating DAG files for submitting bilby parameter
estimation jobs.
"""
import itertools
import os
import shutil
import sys
import subprocess
from pathlib import Path

import pycondor

from .utils import (
    logger,
    parse_args,
    BilbyPipeError,
    DataDump,
    ArgumentsString,
    get_command_line_arguments,
    request_memory_generation_lookup,
)
from . import create_injections
from .input import Input
from .parser import create_parser


class MainInput(Input):
    """ An object to hold all the inputs to bilby_pipe

    Parameters
    ----------
    parser: BilbyArgParser, optional
        The parser containing the command line / ini file inputs
    args_list: list, optional
        A list of the arguments to parse. Defauts to `sys.argv[1:]`

    Attributes
    ----------
    ini: str
        The path to the ini file
    submit: bool
        If true, user-input to also submit the jobs
    label: str
        A label describing the job
    outdir: str
        The path to the directory where output will be stored
    create_summary: bool
        If true, create a summary page
    accounting: str
        The accounting group to use
    coherence_test: bool
        If true, run the coherence test
    detectors: list
        A list of the detectors to include, e.g., ['H1', 'L1']
    unknown_args: list
        A list of unknown command line arguments

    """

    def __init__(self, args, unknown_args):
        logger.debug("Creating new Input object")
        logger.info("Command line arguments: {}".format(args))

        self.unknown_args = unknown_args
        self.ini = args.ini
        self.submit = args.submit
        self.create_plots = args.create_plots
        self.singularity_image = args.singularity_image
        self.outdir = args.outdir
        self.label = args.label
        self.create_summary = args.create_summary
        self.accounting = args.accounting
        self.sampler = args.sampler
        self.detectors = args.detectors
        self.coherence_test = args.coherence_test
        self.n_parallel = args.n_parallel
        self.transfer_files = args.transfer_files
        self.osg = args.osg

        self.waveform_approximant = args.waveform_approximant
        self.likelihood_type = args.likelihood_type
        self.duration = args.duration
        self.prior_file = args.prior_file

        self.webdir = args.webdir
        self.email = args.email
        self.existing_dir = args.existing_dir

        self.run_local = args.local
        self.local_generation = args.local_generation
        self.local_plot = args.local_plot

        self.gps_file = args.gps_file
        self.trigger_time = args.trigger_time
        self.injection = args.injection
        self.injection_file = args.injection_file
        self.n_injection = args.n_injection

        self.request_memory = args.request_memory
        self.request_memory_generation = args.request_memory_generation
        self.request_cpus = args.request_cpus

        self.postprocessing_executable = args.postprocessing_executable
        self.postprocessing_arguments = args.postprocessing_arguments

    @property
    def ini(self):
        return self._ini

    @ini.setter
    def ini(self, ini):
        if os.path.isfile(ini) is False:
            raise FileNotFoundError("No ini file {} found".format(ini))
        self._ini = os.path.relpath(ini)

    @property
    def initialdir(self):
        return os.getcwd()

    @property
    def n_injection(self):
        return self._n_injection

    @n_injection.setter
    def n_injection(self, n_injection):
        if n_injection is None and self.injection and hasattr(self, "gpstimes"):
            logger.info("Injecting signals into segments defined by gpstimes")
            self._n_injection = len(self.gpstimes)
            self.level_A_labels = [
                label + "_injection{}".format(ii)
                for ii, label in enumerate(self.level_A_labels)
            ]
        elif n_injection is not None:
            logger.info("n_injection={}, setting level A jobs".format(n_injection))
            self.n_level_A_jobs = n_injection
            self._n_injection = n_injection
            self.level_A_labels = ["injection{}".format(x) for x in range(n_injection)]
        else:
            logger.info("No injections")
            self._n_injection = None

    @property
    def trigger_time(self):
        return self._trigger_time

    @trigger_time.setter
    def trigger_time(self, trigger_time):
        if trigger_time is not None:
            self._trigger_time = trigger_time
            self.level_A_labels = [str(trigger_time)]
            if self.n_level_A_jobs == 0:
                self.n_level_A_jobs = 1
        else:
            self._trigger_time = None

    @property
    def request_memory(self):
        return self._request_memory

    @request_memory.setter
    def request_memory(self, request_memory):
        logger.info("request_memory={}GB".format(request_memory))
        self._request_memory = "{} GB".format(request_memory)

    @property
    def request_memory_generation(self):
        return self._request_memory_generation

    @request_memory_generation.setter
    def request_memory_generation(self, request_memory_generation):
        if request_memory_generation is None:
            roq = self.likelihood_type == "ROQGravitationalWaveTransient"
            request_memory_generation = request_memory_generation_lookup(
                self.duration, roq=roq
            )
        logger.info("request_memory_generation={}GB".format(request_memory_generation))
        self._request_memory_generation = "{} GB".format(request_memory_generation)

    @property
    def request_cpus(self):
        return self._request_cpus

    @request_cpus.setter
    def request_cpus(self, request_cpus):
        logger.info("request_cpus = {}".format(request_cpus))
        self._request_cpus = request_cpus


class Dag(object):

class Node(object):


def main():
    """ Top-level interface for bilby_pipe """
    parser = create_parser(top_level=True)
    args, unknown_args = parse_args(get_command_line_arguments(), parser)

    inputs = MainInput(args, unknown_args)

    args.outdir = os.path.abspath(args.outdir)
    complete_ini_file = "{}/{}_config_complete.ini".format(inputs.outdir, inputs.label)
    with open(complete_ini_file, "w") as f:
        for key, val in args.__dict__.items():
            print("{}={}".format(key, val), file=f)

    Dag(inputs)

    if len(unknown_args) > 1:
        logger.warning("Unrecognized arguments {}".format(unknown_args))
