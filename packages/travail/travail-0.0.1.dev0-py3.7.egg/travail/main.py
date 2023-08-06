import logging
import argparse
import sys

from toil.job import Job

import travail.preprocess as pp
import travail.test as tt
import travail.utils as tu


def main():
    """
    Travail - hard things are still hard, just slightly better organized.
    """
    logger = logging.getLogger(__name__)
    # -------------------------------  define CLI parser
    #
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    # generate subparsers/subcommands
    subparsers = parser.add_subparsers(dest='command')

    # #################### ------------- `preprocess` ------------- ####################
    parser_preprocess = subparsers.add_parser('preprocess', help='Preprocess gVCF files')
    subparsers_preprocess = parser_preprocess.add_subparsers(dest='preprocess_cmd')

    # 1 - `generate-manifest`
    parser_manifest = subparsers_preprocess.add_parser('generate-manifest',
                                                       help='Generate the manifest file required for combining gVCFs')
    parser_manifest.add_argument('--output', default='preprocess-manifest.tsv',
                                 help='default `preprocess-manifest.tsv` - where to write the manifest file')

    # 2 - `generate-config`
    parser_config = subparsers_preprocess.add_parser('generate-config',
                                                     help='Generate the config file required for combining gVCFs')
    parser_config.add_argument('--output', default='preprocess-config.yml',
                               help='default `preprocess-config.yml` - where to write the config file')

    # 3 - `run-gatk-preprocessing`
    run_gatk_preprocessing = subparsers_preprocess.add_parser('run', help='Run GATK preprocessing using given manifest '
                                                                          'and config file')
    run_gatk_preprocessing.add_argument('config', help='Path to the config file generated with '
                                                       '`generate-config` subcommand')
    run_gatk_preprocessing.add_argument('manifest', help='Path to manifest file generated with '
                                                         '`generate-manifest` subcommand')
    Job.Runner.addToilOptions(run_gatk_preprocessing)  # Add Toil options to the subparser

    # #################### ------------- `analyze` ------------- ####################

    # 1 - `generate-manifest`
    # TODO - this might actually not be needed. Evaluate..
    parser_analyze = subparsers.add_parser('analyze', help='Run main steps of the analysis')
    subparsers_analyze = parser_analyze.add_subparsers(dest='analyze_cmd')
    parser_manifest = subparsers_analyze.add_parser('generate-manifest',
                                                    help='Generate the manifest file required for analysis')

    # 2 - `generate-config`
    parser_config = subparsers_analyze.add_parser('generate-config',
                                                  help='Generate an editable config in the current working directory')

    # 3 - `exomiser`
    parser_exomiser = subparsers_analyze.add_parser('exomiser', help='Run Exomiser on samples within given manifest')
    parser_exomiser.add_argument('--manifest', default='manifest.tsv', type=str,
                                 help='Path to the manifest file, generated with `generate-manifest` subcommand')
    Job.Runner.addToilOptions(parser_exomiser)  # Add Toil options to the subparser

    # 4 - `lirical`
    parser_lirical = subparsers_analyze.add_parser('lirical', help='Run Lirical on samples within given manifest')
    Job.Runner.addToilOptions(parser_lirical)  # Add Toil options to the subparser

    # #################### ------------- `test` ------------- ####################
    # test pipeline that will index the FASTA file and builds the sequence dictionary
    parser_test = subparsers.add_parser('test', help='Run test pipeline')
    subparsers_test = parser_test.add_subparsers(dest='test_cmd')
    test_run = subparsers_test.add_parser('run', help='Run test')
    test_run.add_argument('config', help='Path to the config file generated with generate-config` subcommand')
    Job.Runner.addToilOptions(test_run)
    #
    # -------------------------------  end define CLI parser

    # If no arguments provided, print full help menu
    argv = sys.argv[1:]  # strip away the script name which is the first item in the `argv` list
    if len(argv) == 0:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(argv)

    # -------------------------------- `preprocess` cmd -----------------------------------
    if hasattr(args, 'preprocess_cmd'):
        if args.preprocess_cmd == 'generate-manifest':
            tu.generate_file(pp.generate_manifest, args.output)
            logger.info("Wrote manifest to '{}'".format(args.output))
        elif args.preprocess_cmd == 'generate-config':
            tu.generate_file(pp.generate_config, args.output)
            logger.info("Wrote config file to '{}'".format(args.output))
        elif args.preprocess_cmd == 'run':
            pp.run(args)
        else:
            parser_preprocess.print_help()
    # --------------------------------   `analyze` cmd  -----------------------------------
    elif hasattr(args, 'analyze_cmd'):
        if args.analyze_cmd == 'generate-config':
            logger.info("Generating config file")
        elif args.analyze_cmd == 'exomiser':
            logger.info("Running Exomiser")
        elif args.analyze_cmd == 'lirical':
            logger.info('Running Lirical')
        else:
            parser_analyze.print_help()
    # --------------------------------     `test` cmd   -----------------------------------
    elif hasattr(args, 'test_cmd'):
        if args.test_cmd == 'run':
            tt.run(args)
        else:
            parser_test.print_help()
    else:
        logger.warning("No command was specified")


if __name__ == '__main__':
    main()
