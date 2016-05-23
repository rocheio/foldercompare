"""Compare the content of two folders and create reports of results."""

import csv
import filecmp

def compare(folder1, folder2, output, output_type='both'):
    """Compare the contents of two folders and report it to a file."""

    if output_type not in ('txt', 'csv', 'both'):
        raise ValueError('Value must be "txt", "csv", or "both".')

    report = recursive_dircmp_report(folder1, folder2)

    if output_type in ('txt', 'both'):
        write_to_plain_text(folder1, folder2, output, report)

    if output_type in ('csv', 'both'):
        write_to_csv(folder1, folder2, output, report)


def recursive_dircmp_report(folder1, folder2, prefix='.'):
    """Return a recursive dircmp comparison report as a dictionary."""

    comparison = filecmp.dircmp(folder1, folder2)

    data = {
        'left': [r'{}/{}'.format(prefix, i) for i in comparison.left_only],
        'right': [r'{}/{}'.format(prefix, i) for i in comparison.right_only],
        'both': [r'{}/{}'.format(prefix, i) for i in comparison.common_files],
    }

    for datalist in data.values():
        datalist.sort()

    if comparison.common_dirs:
        for folder in comparison.common_dirs:
            # Update prefix to include new sub_folder
            prefix += '/' + folder

            # Compare common folder and add results to the report
            sub_folder1 = folder1 + '/' + folder
            sub_folder2 = folder2 + '/' + folder
            sub_report = recursive_dircmp_report(sub_folder1, sub_folder2, prefix)

            # Add results from sub_report to main report
            for key, value in sub_report.items():
                data[key] += value

    return data


def write_to_plain_text(folder1, folder2, output, report):
    """Write the comparison data to a plain text file."""

    filename = output + '.txt'
    with open(filename, 'w') as file:
        file.write('COMPARISON OF FILES BETWEEN FOLDERS:\n')
        file.write('\tFOLDER 1: {}\n'.format(folder1))
        file.write('\tFOLDER 2: {}\n'.format(folder2))
        file.write('\n\n')

        file.write('FILES ONLY IN: {}\n'.format(folder1))
        for item in report['left']:
            file.write('\t' + item + '\n')
        if not report['left']:
            file.write('\tNone\n')
        file.write('\n\n')

        file.write('FILES ONLY IN: {}\n'.format(folder2))
        for item in report['right']:
            file.write('\t' + item + '\n')
        if not report['right']:
            file.write('\tNone\n')
        file.write('\n\n')

        file.write('FILES IN BOTH FOLDERS:\n')
        for item in report['both']:
            file.write('\t' + item + '\n')
        if not report['both']:
            file.write('\tNone\n')


def write_to_csv(folder1, folder2, output, report):
    """Write the comparison data to a CSV file for use in Excel."""

    filename = output + '.csv'
    with open(filename, 'w') as file:
        csv_writer = csv.writer(file, dialect='excel', lineterminator='\r')

        # Write header data to the first row
        headers = (
            "Files only in folder '{}'".format(folder1),
            "Files only in folder '{}'".format(folder2),
            "Files in both folders",
        )
        csv_writer.writerow(headers)

        # Order report data to match with headers
        data = (
            report['left'],
            report['right'],
            report['both'],
        )

        # Write comparison data row by row to the CSV
        row_index = 0
        row_max = max(len(column) for column in data)
        while row_index < row_max:
            row = []
            for column_index, _ in enumerate(data):
                # Use data from column if it exists, otherwise use None
                try:
                    row += [data[column_index][row_index]]
                except IndexError:
                    row += [None]

            csv_writer.writerow(row)
            row_index += 1
