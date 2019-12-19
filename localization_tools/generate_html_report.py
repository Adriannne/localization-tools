import os
import re
import time
import pdfkit
import logging
from HTMLTable import HTMLTable
from compare_memory import draw_compare_memory
from compare_pose_kml import draw_pose_kml
# from compare_posreport_kml import draw_posreport_kml
# from compare_offline_data import draw_offline_data


def set_table_style(table):
    table.caption.set_style({
        'font-size': '18px',
    })

    table.set_style({
        'border-collapse': 'collapse',
        'word-break': 'keep-all',
        'white-space': 'nowrap',
        'font-size': '14px',
    })

    table.set_cell_style({
        'border-color': '#66BAB7',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '10px',
    })

    table.set_header_row_style({
        'background-color': '#81C7D4',
        'font-size': '18px',
    })


# def optimize_html_file(html_path):
#     new_html = ""
#     with open(html_path, 'r') as f:
#         for line in f.readlines():
#             if re.search('&lt;', line):
#                 line = re.sub('&lt;', '<', line)
#                 line = re.sub('&gt;', '>', line)
#                 line = re.sub('&#x27;', '\"', line)
#                 new_html += line
#             else:
#                 new_html += line
#     f.close()
#
#     with open(html_path, 'w') as f:
#         f.writelines(new_html)
#     f.close()


def generate_html_file(table, html_path):
    set_table_style(table)
    html = table.to_html()
    with open(html_path, 'w') as f:
        f.writelines(html)
    f.close()

    new_html = ""
    with open(html_path, 'r') as f:
        for line in f.readlines():
            if re.search('&lt;', line):
                line = re.sub('&lt;', '<', line)
                line = re.sub('&gt;', '>', line)
                line = re.sub('&#x27;', '\"', line)
                new_html += line
            else:
                new_html += line
    f.close()

    with open(html_path, 'w') as f:
        f.writelines(new_html)
    f.close()


def generate_pdf_file(html_path):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }

    pdf_path = os.path.splitext(html_path)[0] + ".pdf"
    print(html_path, pdf_path)
    pdfkit.from_file(html_path, pdf_path, options=options)


def generate_compare_table(table, cases, branch_case_dir, master_case_dir, case_name, output_path):
    logging.info('draw_compare_memory(\'{}\', \'{}\', \'{}\', \'{}\')'.format(branch_case_dir, master_case_dir,
                                                                              case_name, output_path))
    draw_compare_memory(branch_case_dir, master_case_dir, case_name, output_path)

    logging.info('draw_pose_kml(\'{}\', \'{}\', \'{}\', \'{}\')'.format(branch_case_dir, master_case_dir, case_name,
                                                                        output_path))
    kml_info = draw_pose_kml(branch_case_dir, master_case_dir, case_name, output_path)

    table.append_data_rows(((
                                "<strong style='color: #66BAB7'>{}</strong><br /><br />{}".format(cases, kml_info),
                                "<img src='compare_pose_kml/{}_distance.png' width='500' />".format(case_name),
                                "<img src='compare_memory/{}_memory.png' width='500' />".format(case_name),
                            ),))


def generate_report_table(table, cases, branch_case_dir, case_name, output_path):
    logging.info('draw_posreport_kml(\'{}\', \'{}\', \'{}\')'.format(branch_case_dir, case_name, output_path))
    draw_posreport_kml(branch_case_dir, case_name, output_path)

    logging.info('draw_offline_data(\'{}\', \'{}\', \'{}\')'.format(branch_case_dir, case_name, output_path))
    draw_offline_data(branch_case_dir, case_name, output_path)

    table.append_data_rows(((
                                cases,
                                "<img src='compare_posreport/{}_prepose.png' width='500' />".format(case_name),
                                "<img src='compare_offline/{}_offline.png' width='500' />".format(case_name),
                            ),))


def compare_two_results(branch_result, master_result, output_path='tmp', html_name='analysis.html'):
    logging.basicConfig(filename='{}/analysis.log'.format(output_path), level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    table = HTMLTable(caption=os.path.splitext(html_name)[0])
    table.append_header_rows((('case', 'compare kml', 'compare memory',),))

    threads = 'multi_ekf'
    row = 1
    for areas in os.listdir(os.path.join(branch_result, threads)):
        table.append_header_rows(((areas, '', '',),))
        table[row][0].attr.colspan = 3
        row = row + 1

        for cases in os.listdir(os.path.join(branch_result, threads, areas)):
            branch_case_dir = os.path.join(branch_result, threads, areas, cases)
            master_case_dir = os.path.join(master_result, threads, areas, cases)
            if os.path.isdir(branch_case_dir) and os.path.isdir(master_case_dir):
                now = int(round(time.time() * 1000))
                now = time.strftime('%Y%m%d%H%M%S', time.localtime(now / 1000))
                case_name = '{}_{}_{}_{}_branch'.format(now, threads, areas, cases)

                generate_compare_table(table, cases, branch_case_dir, master_case_dir, case_name, output_path)
                # generate_report_table(table, cases, branch_case_dir, case_name, output_path)
                row = row + 1
            else:
                logging.warning("error! case {} don't exist in master_result!".format(cases))

    html_path = os.path.join(output_path, html_name)
    generate_html_file(table, html_path)
    generate_pdf_file(html_path)


if __name__ == '__main__':
    master_result = '/Users/user/localization/RDB-46282/result_41'
    branch_result = '/Users/user/localization/RDB-46282/result_branch'
    output_path = '/Users/user/localization/RDB-46282/output'
    html_name = 'RDB-46282_coordinate_modification.html'

    os.system('mkdir -p {}'.format(output_path))
    compare_two_results(branch_result, master_result, output_path, html_name)
    print('finished')