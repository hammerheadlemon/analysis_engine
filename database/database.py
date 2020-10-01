import sqlite3
from datamaps.api import project_data_from_master
from typing import Dict


#  what's the best method of integration this into code. Could as a variable but starts making
#  variable list long and untidy. Does it need to be a variable as doesn't change at local level.
def project_id_numbers(project_name: str) -> int:
    id_dict = {'Sea of Tranquility': 1,
               'Apollo 11': 2,
               'Apollo 13': 3,
               'Falcon 9': 4,
               'Columbia': 5,
               'Mars': 6}

    return id_dict[project_name]


#  same question as for project_id_numbers
def project_group_ref(project_name: str) -> str:
    group_dict = {'Sea of Tranquility': "Rail Group",
                  'Apollo 11': "HSMRPG",
                  'Apollo 13': "RPE",
                  'Falcon 9': "AMIS",
                  'Columbia': "AMIS",
                  'Mars': "Rail Group"}

    return group_dict[project_name]


def create_connect_db(db_name):
    conn = sqlite3.connect(db_name + '.db')
    return conn


def import_master_to_db(db_path: str, masters: list) -> None:
    """
    this function puts master data into a dB via a python dictionary
    """
    # m = project_data_from_master(master_path, 4, 2019)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    #  insert group types
    group_list = ["Rail Group", "HSMRPG", "RPE", "AMIS"]
    for g in group_list:
        c.execute(f"INSERT INTO dft_group (name) VALUES ('{g}')")
    #  insert milestone types
    milestone_type_list = ["Approval", "Assurance", "Project"]
    for t in milestone_type_list:
        c.execute(f"INSERT INTO milestone_type (type) VALUES ('{t}')")

    for m in masters:
        import_project_to_master_db(m, c)

    for m in masters:
        import_quarter_to_master_db(m, c)

    for m in masters:
        import_milestone_to_master_db(m, c)

    conn.commit()


def import_quarter_to_master_db(master: Dict[str, str], c) -> None:
    """
    this function places quarter data into the dB.
    """
    c.execute(f"INSERT INTO quarter (quarter_id, quarter_number) VALUES ("
              f"'{master.quarter}', '{master.quarter.quarter}')")


def import_project_to_master_db(master: Dict[str, str], c) -> None:
    """
    this function places project data into the dB.
    """
    for project in master.projects:
        try:
            c.execute(f"INSERT INTO project (group_name, project_id, name) "
                      f"VALUES ("
                      f"'{project_group_ref(project)}', "
                      f"'{master.data[project]['DFT ID Number']}', '{project}')")
        except sqlite3.IntegrityError:
            pass


def import_milestone_to_master_db(master: Dict[str, str], c) -> None:
    """
    this function places milestone data into the dB.
    """
    for project in master.projects:
        for i in range(1, 68):
            #  Approval milestones
            m_type_as = "Approval MM" + str(i)
            if m_type_as in list(master.data[project].keys()):
                #  note string amended to remove ' and replace with ''
                n = master.data[project]["Approval MM" + str(i) + " Notes"]
                note = n.replace("'", "''")
                #  question. does {} need '{}' around them? In what instances.
                c.execute(
                    f"INSERT INTO milestone (milestone_type, quarter_id, project_id, project_name, "
                    f"name, gov_type, ver_no, orig_baseline, forecast_actual, variance, status, notes,"
                    f"lod, crit_path) "
                    f"VALUES ('Approval', '{master.quarter}', "
                    f"'{master.data[project]['DFT ID Number']}', '{project}', "
                    f"'{master.data[project]['Approval MM' + str(i)]}', "
                    f"'{master.data[project]['Approval MM' + str(i) + ' Gov Type']}',"
                    f"'{master.data[project]['Approval MM' + str(i) + ' Ver No']}', "
                    f"'{master.data[project]['Approval MM' + str(i) + ' Original Baseline']}',"
                    f"'{master.data[project]['Approval MM' + str(i) + ' Forecast / Actual']}',"
                    f"'{master.data[project]['Approval MM' + str(i) + ' Variance']}',"
                    f"'{master.data[project]['Approval MM' + str(i) + ' Status']}',"
                    f"'{note}', 'None', 'None')")
            #  Assurance milestones
            m_type_as = "Assurance MM" + str(i)
            if m_type_as in list(master.data[project].keys()):
                #  note string amended to remove ' and replace with ''
                n = master.data[project]["Assurance MM" + str(i) + " Notes"]
                note = n.replace("'", "''")
                #  question. does {} need '{}' around them? In what instances.
                c.execute(
                    f"INSERT INTO milestone (milestone_type, quarter_id, project_id, project_name, "
                    f"name, gov_type, ver_no, orig_baseline, forecast_actual, variance, status, notes,"
                    f"lod, crit_path) "
                    f"VALUES ('Assurance', '{master.quarter}', "
                    f"'{master.data[project]['DFT ID Number']}', '{project}', "
                    f"'{master.data[project]['Assurance MM' + str(i)]}', "
                    f"'None',"
                    f"'None', "
                    f"'{master.data[project]['Assurance MM' + str(i) + ' Original Baseline']}',"
                    f"'{master.data[project]['Assurance MM' + str(i) + ' Forecast - Actual']}',"
                    f"'{master.data[project]['Assurance MM' + str(i) + ' Variance']}',"
                    f"'{master.data[project]['Assurance MM' + str(i) + ' Status']}',"
                    f"'{note}', '{master.data[project]['Assurance MM' + str(i) + ' LoD']}', 'None')")
            #  Approval milestones
            m_type_as = "Project MM" + str(i)
            if m_type_as in list(master.data[project].keys()):
                #  note string amended to remove ' and replace with ''
                n = master.data[project]["Project MM" + str(i) + " Notes"]
                note = n.replace("'", "''")
                #  question. does {} need '{}' around them? In what instances.
                c.execute(
                    f"INSERT INTO milestone (milestone_type, quarter_id, project_id, project_name, "
                    f"name, gov_type, ver_no, orig_baseline, forecast_actual, variance, status, notes,"
                    f"lod, crit_path) "
                    f"VALUES ('Project', '{master.quarter}', "
                    f"'{master.data[project]['DFT ID Number']}', '{project}', "
                    f"'{master.data[project]['Project MM' + str(i)]}', "
                    f"'None',"
                    f"'None', "
                    f"'{master.data[project]['Project MM' + str(i) + ' Original Baseline']}',"
                    f"'{master.data[project]['Project MM' + str(i) + ' Forecast - Actual']}',"
                    f"'{master.data[project]['Project MM' + str(i) + ' Variance']}',"
                    f"'{master.data[project]['Project MM' + str(i) + ' Status']}',"
                    f"'{note}', 'None',"
                    f"'{master.data[project]['Project MM' + str(i) + ' CP']}')")


#  create master dB.
def create_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    DROP TABLE IF EXISTS quarter;
    """)
    c.execute("""
    DROP TABLE IF EXISTS dft_group;
    """)
    c.execute("""
    DROP TABLE IF EXISTS project;
    """)
    c.execute("""
    DROP TABLE IF EXISTS milestone_type;
    """)
    c.execute("""
    DROP TABLE IF EXISTS milestone;
    """)

    c.execute("""CREATE TABLE quarter
            (id INTEGER PRIMARY KEY,
            quarter_id text,
            quarter_number integer)""")

    c.execute("""CREATE UNIQUE INDEX i1 ON quarter
            (quarter_id)""")

    c.execute("""CREATE TABLE dft_group
            (id INTEGER PRIMARY KEY,
            name text)""")

    c.execute("""CREATE UNIQUE INDEX i2 ON dft_group
                (name)""")

    c.execute("""CREATE TABLE project
            (id INTEGER PRIMARY KEY,
            group_name text,
            project_id integer,
            name text,
            UNIQUE (project_id, name),
            FOREIGN KEY(group_name) REFERENCES dft_group(name))""")

    c.execute("""CREATE UNIQUE INDEX i3 ON project
                (project_id, name)""")

    c.execute("""CREATE TABLE milestone_type
            (id INTEGER PRIMARY KEY,
            type text)""")

    c.execute("""CREATE UNIQUE INDEX i4 ON milestone_type
                (type)""")

    c.execute("""CREATE TABLE milestone
            (id INTEGER PRIMARY KEY,
            milestone_type text,
            quarter_id integer,
            project_id integer,
            project_name text,
            name text,
            gov_type text,
            ver_no real,
            orig_baseline text,
            forecast_actual text,
            variance real,
            status text,
            notes text,
            lod text,
            crit_path text,
            FOREIGN KEY(quarter_id) REFERENCES quarter(quarter_id),
            FOREIGN KEY(project_id, project_name) REFERENCES project(project_id, name),
            FOREIGN KEY(milestone_type) REFERENCES milestone_type(type)
            )""")

    conn.commit()
    conn.close()




#  create a new table in vfm db.
def create_vfm_table(db_name, insert_quarter):
    conn = sqlite3.connect(db_name + '.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE '{quarter}'
            (project_name text,
            project_group text,
            npv real,
            adjusted_bcr real,
            initial_bcr real,
            vfm_cat_single text,
            pvc real,
            pvb real)""".format(quarter=insert_quarter))

    conn.commit()
    conn.close()

#  gets vfm data values from master data in excel wbs.
def get_vfm_values(masters):
    output_list = []
    for master in masters:
        quarter = master.quarter
        for project in master.projects:
            group = master.data[project]['DfT Group']
            npv = master.data[project]['NPV for all projects ' \
                                       'and NPV for programmes if available']
            adjusted_bcr = master.data[project]['Adjusted Benefits Cost Ratio (BCR)']
            initial_bcr = master.data[project]['Initial Benefits Cost Ratio (BCR)']
            vfm_cat_single = master.data[project]['VfM Category single entry']
            pvc = master.data[project]['Present Value Cost (PVC)']
            pvb = master.data[project]['Present Value Benefit (PVB)']
            output_list.append((str(quarter),
                                project,
                                group,
                                npv,
                                adjusted_bcr,
                                initial_bcr,
                                vfm_cat_single,
                                pvc,
                                pvb))

    return output_list


#  returns vfm list of tuples for specified quarter
def get_quarter_values(vfm_list, quarter):
    output_list = []
    for i in vfm_list:
        if i[0] == quarter:
            output_list.append(i[1:])

    return output_list


#  insert many values into vfm db.
#  To be further abstracted for all dbs.
def insert_many_vfm_db(db_name, quarter, vfm_list):
    conn = sqlite3.connect(db_name + '.db')
    c = conn.cursor()
    c.executemany("INSERT INTO '{table}' VALUES (?,?,?,?,?,?,?,?)".format(table=quarter), vfm_list)
    conn.commit()
    conn.close()


#  for querying db in python
def query_db(db_path, key, quarter):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    c.execute("SELECT {key} FROM {table}".format(key=key, table=quarter))
    result = c.fetchall()

    conn.commit()
    conn.close()

    return result


#  returns a list of project names
def get_project_names(db_path, quarter):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    names = c.execute("SELECT project_name FROM '{table}'".format(table=quarter)).fetchall()
    conn.commit()
    conn.close()
    return names


#  Converts a db into a python dictionary when give a db and qrt list.
def convert_db_python_dict(db_path, quarter_list):
    conn = sqlite3.connect(db_path)

    # This is the important part, here we are setting row_factory property of
    # connection object to sqlite3.Row(sqlite3.Row is an implementation of
    # row_factory)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    output_dict = {}
    for quarter in quarter_list:
        inner_dict = {}
        project_names = get_project_names(db_path, quarter)
        for project in project_names:
            c.execute("select * from '{table}' WHERE project_name = '{p}'".format(table=quarter, p=project))
            result = [dict(row) for row in c.fetchall()][0]  # [0] there as output is dict in a list
            inner_dict[project] = result

        output_dict[quarter] = inner_dict

    conn.commit()
    conn.close()

    return output_dict
