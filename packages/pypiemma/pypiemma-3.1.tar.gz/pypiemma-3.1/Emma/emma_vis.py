"""
Emma - Emma Memory and Mapfile Analyser
Copyright (C) 2019 The Emma authors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

# Emma Memory and Mapfile Analyser - visualiser

import gc
import sys
import os
import timeit
import datetime
import argparse
import pandas

from pypiscout.SCout_Logger import Logger as sc

from Emma.shared_libs.stringConstants import *                           # pylint: disable=unused-wildcard-import,wildcard-import
import Emma.shared_libs.emma_helper
import Emma.emma_vis_libs.dataVisualiserSections
import Emma.emma_vis_libs.dataVisualiserObjects
import Emma.emma_vis_libs.dataVisualiserCategorisedSections
import Emma.emma_vis_libs.dataVisualiserMemoryMap
import Emma.emma_vis_libs.dataReports
import Emma.emma_vis_libs.helper


# Set display settings for unwrapped console output (pandas)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.expand_frame_repr', False)


def main(arguments):
    """
    Emma visualiser application
    :param arguments: parsed arguments
    :return: None
    """
    # Setup SCout
    sc(invVerbosity=-1, actionWarning=(lambda : sys.exit(-10) if arguments.Werror is not None else None), actionError=lambda : sys.exit(-10))

    sc().header("Emma Memory and Mapfile Analyser - Visualiser", symbol="/")

    # Start and display time measurement
    TIME_START = timeit.default_timer()
    sc().info("Started processing at", datetime.datetime.now().strftime("%H:%M:%S"))

    imageFile = Emma.emma_vis_libs.helper.getLastModFileOrPrompt(FILE_IDENTIFIER_SECTION_SUMMARY, arguments.inOutPath, arguments.quiet, arguments.append, arguments.noprompt)
    moduleFile = Emma.emma_vis_libs.helper.getLastModFileOrPrompt(FILE_IDENTIFIER_OBJECT_SUMMARY, arguments.inOutPath, arguments.quiet, arguments.append, arguments.noprompt)
    objectsInSectionsFile = Emma.emma_vis_libs.helper.getLastModFileOrPrompt(FILE_IDENTIFIER_OBJECTS_IN_SECTIONS, arguments.inOutPath, arguments.quiet, arguments.append, arguments.noprompt)

    resultsPath = Emma.shared_libs.emma_helper.joinPath(arguments.inOutPath, OUTPUT_DIR_VISUALISER)        # We don't have to check the existance of this path since this was done during parseArgs
    Emma.shared_libs.emma_helper.mkDirIfNeeded(resultsPath)

    # Init classes for summaries
    consumptionObjectsInSections = Emma.emma_vis_libs.dataVisualiserMemoryMap.MemoryMap(projectPath=arguments.projectDir,
                                                                                        fileToUse=objectsInSectionsFile,
                                                                                        resultsPath=resultsPath)
    consumptionObjectsInSections.plotPieChart(plotShow=False)

    # Image Summary object
    sc().info("Analysing", imageFile)
    consumptionImage = Emma.emma_vis_libs.dataVisualiserSections.ImageConsumptionList(projectPath=arguments.projectDir,
                                                                                      fileToUse=imageFile,
                                                                                      resultsPath=resultsPath)

    # Module Summary object
    sc().info("Analysing", moduleFile)
    try:
        consumptionModule = Emma.emma_vis_libs.dataVisualiserObjects.ModuleConsumptionList(projectPath=arguments.projectDir,
                                                                                           fileToUse=moduleFile,
                                                                                           resultsPath=resultsPath)
    except ValueError:
        sc().error("Data does not contain any module/object entry - exiting...")

    # Object for visualisation fo image and module summary
    categorisedImage = Emma.emma_vis_libs.dataVisualiserCategorisedSections.CategorisedImageConsumptionList(resultsPath=resultsPath,
                                                                                                            projectPath=arguments.projectDir,
                                                                                                            statsTimestamp=consumptionImage.statsTimestamp,
                                                                                                            imageSumObj=consumptionImage,
                                                                                                            moduleSumObj=consumptionModule)

    # Do prints and plots
    consumptionImage.plotByMemType(plotShow=False)

    # Prevent out of memory errors (-> `AssertionError: Unexpected exception: In RendererAgg: Out of memory`)
    gc.collect()

    sc().info("\n", consumptionImage.calcConsumptionByMemType())

    # FIXME: Deactivated; colours of legend in figure not correct - possibly this figure is not even needed/useful (MSc)
    # categorisedImage.plotNdisplay(plotShow=False)

    # Save the categorised sections as csv
    if arguments.categorised_image_csv:
        categorisedImage.categorisedImagetoCSV()

    # Write each report to file if append mode in parsedArguments is selected
    if arguments.append:
        sc().info("Appending report...")
        consumptionImage.writeReportToFile()
        report = Emma.emma_vis_libs.dataReports.Reports(projectPath=arguments.projectDir)
        report.plotNdisplay(plotShow=False)

    # Create a Markdown overview document and add all parts to it
    if arguments.overview:
        sc().info("Generating markdown report...")
        markdownFilePath = consumptionImage.createMarkdownOverview()
        consumptionModule.appendModuleConsumptionToMarkdownOverview(markdownFilePath)
        consumptionImage.appendSupplementToMarkdownOverview(markdownFilePath)
        sc().info("Generating html report...")
        Emma.shared_libs.emma_helper.convertMarkdownFileToHtmlFile(markdownFilePath, (os.path.splitext(markdownFilePath)[0] + ".html"))

    # Stop and display time measurement
    TIME_END = timeit.default_timer()
    sc().info("Finished job at:", datetime.datetime.now().strftime("%H:%M:%S"), "(duration: " + "{0:.2f}".format(TIME_END - TIME_START) + "s)")


def initParser():
    """
    Prepare the parser for Emma
    We need this as a separate function for the top level sub commands (argparse).
    :return: Set-up parser
    """
    parser = argparse.ArgumentParser(
        prog="Emma Visualiser",
        description="Data aggregation and visualisation tool for Emma Memory and Mapfile Analyser (Emma).",
        epilog=EPILOG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--version",
        help="Display the version number.",
        action="version",
        version="%(prog)s, Version: " + EMMA_VISUALISER_VERSION
    )
    parser.add_argument(
        "--projectDir",
        "-p",
        required=True,
        help="Path to directory holding the config files. The project name will be derived from this folder name,",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        help="Automatically accepts last modified .csv file in ./memStats folder",
        action="store_true"
    )
    parser.add_argument(
        "--append",
        help="Append reports to file in ./results folder",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--inOutDir",
        "-i",
        help="Path containing the memStats directory (-> Emma output). If not given the `project` directory will be used.",
        default=None
    )
    parser.add_argument(
        "--subDir",
        help="Sub-directory of `inOutDir` where the Emma Visualiser results will be stored. If not given results will be stored in `inOutDir`.",
        default=None
    )
    parser.add_argument(
        "--overview",
        help="Create a .html overview.",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--categorised_image_csv",
        "-cat_img",
        help="Save a .csv of categories found inside the image summary",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--noprompt",
        help="Exit program with an error if a user prompt occurs; useful for CI systems",
        action="store_true",
        default=False
    )
    return parser


def parseArgs(arguments=""):
    """
    Argument parser
    :param arguments: List of strings specifying the arguments to be parsed
    :return: Argparse object
    """
    parser = initParser()

    parsedArguments = Emma.shared_libs.emma_helper.parseGivenArgStrOrStdIn(arguments, parser)

    # Prepare final paths
    parsedArguments.inOutPath = ""

    # Check given paths
    if parsedArguments.projectDir is None:                  # This should not happen since it is a required argument
        sc().error("No project path given. Exiting...")
    else:
        parsedArguments.projectDir = Emma.shared_libs.emma_helper.joinPath(parsedArguments.projectDir)           # Unify path
        Emma.shared_libs.emma_helper.checkIfFolderExists(parsedArguments.projectDir)

        parsedArguments.inOutPath = parsedArguments.projectDir
    if parsedArguments.inOutDir is None:
        parsedArguments.inOutDir = parsedArguments.projectDir
    else:
        parsedArguments.inOutDir = Emma.shared_libs.emma_helper.joinPath(parsedArguments.inOutDir)               # Unify path
        Emma.shared_libs.emma_helper.checkIfFolderExists(parsedArguments.inOutDir)

        parsedArguments.inOutPath = parsedArguments.inOutDir
        if parsedArguments.subDir is None:
            parsedArguments.subDir = ""
        else:
            parsedArguments.subDir = Emma.shared_libs.emma_helper.joinPath(parsedArguments.subDir)               # Unify path

            joinedInputPath = Emma.shared_libs.emma_helper.joinPath(parsedArguments.inOutDir, parsedArguments.subDir)
            Emma.shared_libs.emma_helper.checkIfFolderExists(joinedInputPath)
            parsedArguments.inOutPath = joinedInputPath

    # Clean-up paths
    del parsedArguments.subDir
    del parsedArguments.inOutDir

    return parsedArguments


def runEmmaVis():
    """
    Runs Emma Visualiser application
    :return: None
    """
    # Parsing the command line arguments
    parsedArguments = parseArgs()

    # Execute Emma Visualiser
    main(parsedArguments)


if __name__ == "__main__":
    runEmmaVis()
