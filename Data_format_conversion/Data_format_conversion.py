import pprint
import os
import sys
import html
import datetime
from bs4 import BeautifulSoup

utils_path = os.path.abspath('utils')
sys.path.append(utils_path)

#Load psycopg to connect to PostgreSQL
from db_interface import PGDBInterface


def print_lines(text):
    """
    Print text line by line using line numbers
    """
    count = 1
    for line in text.split("\n"):
        print(count, line)
        count += 1


def parse_uspto_file(bs, logging=False):
    """
    Analyze USPTO patents in BeautifulSoup objects.
    """

    # Check for existence before attempting to access elements to avoid throwing exceptions

    # Extract title
    try:
        publication_title = bs.find('invention-title').text
    except Exception as e:
        print(f"Error extracting publication_title: {e}")
        publication_title = ""

    # Extract patent publication number
    try:
        publication_num = bs['file'].split("-")[0]
    except Exception as e:
        print(f"Error extracting publication_number: {e}")
        publication_num = ""

    # Extract patent application number
    try:
        application_num = bs.find('application-reference').find('doc-number').text
    except Exception as e:
        print(f"Error extracting application_number: {e}")
        application_num = ""
    print('Patent application number:', application_num)
    application_type = bs.find('application-reference')['appl-type']

    try:
        application_type = bs.find('application-reference')['appl-type']
    except Exception as e:
        print(f"Error extracting application_type: {e}")
        application_type = ""

    # International Patent Classification (IPC) document:
    # https://www.wipo.int/classifications/ipc/en/
    sections = {}
    section_classes = {}
    section_class_subclasses = {}
    section_class_subclass_groups = {}
    for classes in bs.find_all('classifications-ipcr'):
        for el in classes.find_all('classification-ipcr'):
            try:
                section = el.find('section').text
            except Exception as e:
                print(f"Error extracting section: {e}")
                section = ""

            classification = section

            try:
                a = el.find('class').text
            except Exception as e:
                print(f"Error extracting class: {e}")
                a = ""

            try:
                b = el.find('subclass').text
            except Exception as e:
                print(f"Error extracting subclass: {e}")
                b = ""

            classification += a
            classification += b

            try:
                c = el.find('main-group').text
            except Exception as e:
                print(f"Error extracting main_gropu: {e}")
                c = ""


            group = c + "/"

            try:
                d = el.find('subgroup').text
            except Exception as e:
                print(f"Error extracting subgroup: {e}")
                d = ""

            group += d

            sections[section] = True
            section_classes[section + a] = True
            section_class_subclasses[classification] = True

    authors = []
    for parties in bs.find_all('us-parties'):
        for applicants in parties.find_all('us-applicants'):
            for el in applicants.find_all('addressbook'):
                try:
                    first_name = el.find('first-name').text
                except Exception as e:
                    print(f"Error extracting first-name: {e}")
                    first_name = ""

                try:
                    last_name = el.find('last-name').text
                except Exception as e:
                    print(f"Error extracting last-name: {e}")
                    last_name = ""

                authors.append(first_name + " " + last_name)

    abstracts = []
    for el in bs.find_all('abstract'):
        try:
            aa = el.text
        except Exception as e:
            print(f"Error extracting el.text: {e}")
            aa = ""
        abstracts.append(aa.strip('\n'))

    descriptions = []
    for el in bs.find_all('description'):
        try:
            bb = el.text
        except Exception as e:
            print(f"Error extracting el.text: {e}")
            bb = ""
        descriptions.append(bb.strip('\n'))

    claims = []
    for el in bs.find_all('claim'):
        try:
            cc = el.text
        except Exception as e:
            print(f"Error extracting el.text: {e}")
            cc = ""
        claims.append(cc.strip('\n'))

    uspto_patent = {
        "publication_title": publication_title,
        "publication_number": publication_num,
        "application_num": application_num,
        "application_type": application_type,
        "authors": authors,  # list
        "sections": list(sections.keys()),
        "section_classes": list(section_classes.keys()),
        "section_class_subclasses": list(section_class_subclasses.keys()),
        "section_class_subclass_groups": list(section_class_subclass_groups.keys()),
        "abstract": abstracts,  # list
        "descriptions": descriptions,  # list
        "claims": claims  # list
    }

    if logging:

        # print(bs.prettify())

        print("Filename:", filename)
        print("\n\n")
        print("\n--------------------------------------------------------\n")

        print("USPTO Invention Title:", publication_title)
        print("USPTO Publication Number:", publication_num)
        print("USPTO Application_num:", application_num)
        print("USPTO Application Type:", application_type)

        count = 1
        for classification in section - class_subclass_groups:
            print("USPTO Classification #" + str(count) + ": " + classification)
            count += 1
        print("\n")

        count = 1
        for author in authors:
            print("Inventor #" + str(count) + ": " + author)
            count += 1

        print("\n--------------------------------------------------------\n")

        print("Abstract:\n-----------------------------------------------")
        for abstract in abstracts:
            print(abstract)

        print("Description:\n-----------------------------------------------")
        for description in descriptions:
            print(description)

        print("Claims:\n-----------------------------------------------")
        for claim in claims:
            print(claim)

    title = "Shower shield system for bathroom shower drain areaways"
    if bs.find('invention-title').text == title:
        print(bs)
        exit()

    return uspto_patent


def write_to_db(uspto_patent, db=None):
    """
    pp = pprint.PrettyPrinter(indent=2)
    for key in uspto_patent:
        if type(uspto_patent[key]) == list:
            if key == "section_class_subclass_groups":
                print("\n--------------------------------")
                print(uspto_patent['publication_title'])
                print(uspto_patent['publication_number'])
                print(uspto_patent['publication_date'])
                print(uspto_patent['sections'])
                print(uspto_patent['section_classes'])
                print(uspto_patent['section_class_subclasses'])
                print(uspto_patent['section_class_subclass_groups'])
                print("--------------------------------")
    """

    # Will be used for creating d_at and updating d_at times
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Input database
    uspto_db_entry = [
        uspto_patent['publication_title'],
        uspto_patent['publication_number'],
        uspto_patent['application_num'],
        uspto_patent['application_type'],
        ','.join(uspto_patent['authors']),
        ','.join(uspto_patent['sections']),
        ','.join(uspto_patent['section_classes']),
        ','.join(uspto_patent['section_class_subclasses']),
        ','.join(uspto_patent['section_class_subclass_groups']),
        '\n'.join(uspto_patent['abstract']),
        '\n'.join(uspto_patent['descriptions']),
        '\n'.join(uspto_patent['claims']),
        current_time,
        current_time
    ]

    # ON CONFLICT UPDATES TO DB
    uspto_db_entry += [
        uspto_patent['publication_title'],
        uspto_patent['application_num'],
        uspto_patent['application_type'],
        ','.join(uspto_patent['authors']),
        ','.join(uspto_patent['sections']),
        ','.join(uspto_patent['section_classes']),
        ','.join(uspto_patent['section_class_subclasses']),
        ','.join(uspto_patent['section_class_subclass_groups']),
        '\n'.join(uspto_patent['abstract']),
        '\n'.join(uspto_patent['descriptions']),
        '\n'.join(uspto_patent['claims']),
        current_time
    ]

    db_cursor = None
    if db is not None:
        db_cursor = db.obtain_db_cursor()

    if db_cursor is not None:
        db_cursor.execute("INSERT INTO uspto_patents ("
                          + "publication_title, publication_number, "
                          + "application_num, publication_type, "
                          + "authors, sections, section_classes, "
                          + "section_class_subclasses, "
                          + "section_class_subclass_groups, "
                          + "abstract, description, claims, "
                          + "created_at, updated_at"
                          + ") VALUES ("
                          + "%s, %s, %s, %s, %s, %s, %s, %s, "
                          + "%s, %s, %s, %s, %s, %s) "
                          + "ON CONFLICT(publication_number) "
                          + "DO UPDATE SET "
                          + "publication_title=%s, "
                          + "publication_date=%s, "
                          + "publication_type=%s, "
                          + "authors=%s, "
                          + "sections=%s, section_classes=%s, "
                          + "section_class_subclasses=%s, "
                          + "section_class_subclass_groups=%s, "
                          + "abstract=%s, description=%s, "
                          + "claims=%s, updated_at=%s", uspto_db_entry)

    return


arg_filenames = ['../ipg190101.xml'] # Specify file name
if len(sys.argv) > 1:
    arg_filenames = sys.argv[1:]

filenames = []
for filename in arg_filenames:
    # Load listed directories
    if os.path.isdir(filename):
        print("directory", filename)
        for dir_filename in os.listdir(filename):
            directory = filename
            if directory[-1] != "/":
                directory += "/"
            filenames.append(directory + dir_filename)

            # Load listed files
    if ".xml" in filename:
        filenames.append(filename)

print("LOADING FILES TO PARSE\n----------------------------")
for filename in filenames:
    print(filename)

db_config_file = "config/postgres.tsv"
db = PGDBInterface(config_file=db_config_file)
db.silent_logging = True

count = 1
success_count = 0
errors = []
for filename in filenames:
    if ".xml" in filename:

        xml_text = html.unescape(open(filename, 'r').read())

        for patent in xml_text.split("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"):

            if patent is None or patent == "":
                continue

            bs = BeautifulSoup(patent, 'lxml')

            if bs.find('sequence-cwu') is not None:
                continue  # Skip DNA sequence documents

            application = bs.find('us-patent-application')
            if application is None:  # If no application, search for grant
                application = bs.find('us-patent-grant')
            title = "None"

            # Add a new try except block
            try:
                title = application.find('invention-title').text
            except Exception as e:
                print("Error", count, e)

            # Print out debugging information before attempting to perform database writes
            print(count, filename, title)

            try:
                uspto_patent = parse_uspto_file(application)
                write_to_db(uspto_patent, db=db)
                success_count += 1
            except Exception as e:
                errors.append((count, title, e))
                print(e)

            count += 1

            # break

print("\n\nErrors\n------------------------\n")
for e in errors:
    print(e)

print("Success Count:", success_count)
print("Error Count:", len(errors))
