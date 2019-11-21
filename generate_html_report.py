import os
import re
import time
import pdfkit
import logging
import compare_posreport_kml
from HTMLTable import HTMLTable
from compare_kml import compare_kml
from draw_memory import draw_compare_memory


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


def optimize_html_file(html_path):
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
    pdfkit.from_file(html_path, pdf_path, options=options)


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
            print('a')
            branch_case_dir = os.path.join(branch_result, threads, areas, cases)
            master_case_dir = os.path.join(master_result, threads, areas, cases)
            if os.path.isdir(master_case_dir):
                print('b')
                now = int(round(time.time() * 1000))
                now = time.strftime('%Y%m%d%H%M%S', time.localtime(now / 1000))
                case_name = '{}_{}_{}_{}_branch'.format(now, threads, areas, cases)

                logging.info('draw_compare_memory(\'{}\', \'{}\', \'{}\', \'{}\')'.format(branch_case_dir, master_case_dir,
                                                                                   case_name, output_path))
                draw_compare_memory(branch_case_dir, master_case_dir, case_name, output_path)

                logging.info('compare_kml(\'{}\', \'{}\', \'{}\', \'{}\')'.format(branch_case_dir, master_case_dir, case_name,
                                                                           output_path))
                kml_info = compare_kml(branch_case_dir, master_case_dir, case_name, output_path)

                table.append_data_rows(((
                                            "<strong style='color: #66BAB7'>{}</strong><br /><br />{}".format(cases, kml_info),
                                            "<img src='compare_kml/{}_distance.png' width='500' />".format(case_name),
                                            "<img src='compare_memory/{}_memory.png' width='500' />".format(case_name),
                                        ),))

                # logging.info('compare_kml(\'{}\', \'{}\', \'{}\')'.format(branch_case_dir, case_name, output_path))
                # compare_posreport_kml.compare_kml(branch_case_dir, case_name, output_path)
                #
                # logging.info('compare_offline(\'{}\', \'{}\', \'{}\')'.format(branch_case_dir, case_name, output_path))
                # tmp_offline.compare_offline(branch_case_dir, case_name, output_path)
                #
                # table.append_data_rows(((
                #                             cases,
                #                             "<img src='compare_posreport/{}_prepose.png' width='500' />".format(case_name),
                #                             "<img src='compare_offline/{}_offline.png' width='500' />".format(case_name),
                #                         ),))
                row = row + 1
            else:
                logging.warning("error! case {} don't exist in master_result!".format(cases))

    set_table_style(table)
    html = table.to_html()
    html_path = os.path.join(output_path, html_name)
    with open(html_path, 'w') as f:
        f.writelines(html)
    f.close()

    optimize_html_file(html_path)
    generate_pdf_file(html_path)


if __name__ == '__main__':
    master_result = '/home/user/localization/RDB-46015/master_result'
    branch_result = '/home/user/localization/test_jlrdb41/result_master'
    output_path = '/home/user/localization/test_jlrdb41/output'
    html_name = 'RDB-46015_contrast_testing_xy.html'

    os.system('mkdir -p {}'.format(output_path))
    compare_two_results(branch_result, master_result, output_path, html_name)
    print('finished')