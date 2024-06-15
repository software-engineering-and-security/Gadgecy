import os.path
import pandas as pd
import numpy as np
import functools
import json


def flatten(l):
    flat_list = []
    for ll in l:
        flat_list = flat_list + ll
    return flat_list


def jdk_sort_function(a, b):

    if "harmony" in a: return -1
    if "harmony" in b: return 1

    jvm_type_a = a.split("-")[0]
    jvm_type_b = b.split("-")[0]

    if a > b:
        return -1
    elif a < b:
        return 1

    major_version_a = int(
        a.replace("jdk1.", "").replace("jdk-", "").replace("jdk", "").replace("ibm-", "").replace("temurin-", "").replace("openjdk-", "").split("u")[0].split(".")[0])
    major_version_b = int(
        b.replace("jdk1.", "").replace("jdk-", "").replace("jdk", "").replace("ibm-", "").replace("temurin-", "").replace("openjdk-", "").split("u")[0].split(".")[0])

    if major_version_b != major_version_a:
        return major_version_a - major_version_b

    if major_version_a <= 8:
        if "ibm" or "temurin" in a:
            return int(a.split("u")[1].split("-")[0]) - int(b.split("u")[1].split("-")[0])

        minor_version_a = 0 if not "_" in a else int(a.split("_")[1])
        minor_version_b = 0 if not "_" in b else int(b.split("_")[1])
        return minor_version_a - minor_version_b

    minor_version_a = 0 if len(a.split(".")) <= 1 else int(a.split(".")[2].split("+")[0])
    minor_version_b = 0 if len(b.split(".")) <= 1 else int(b.split(".")[2].split("+")[0])

    return minor_version_a - minor_version_b


def version_sort_function(a, b):
    version_nums_a = a.split(".")
    version_nums_b = b.split(".")

    if int(version_nums_a[0]) > 10000 : version_nums_a = ["0"] + version_nums_a
    if int(version_nums_b[0]) > 10000: version_nums_b = ["0"] + version_nums_b

    for i in range(0, len(version_nums_a)):
        try:
            if int(version_nums_a[i]) == int(version_nums_b[i]):
                continue
            return int(version_nums_a[i]) - int(version_nums_b[i])
        except:
            return len(version_nums_a) - len(version_nums_b)

    return -1


def parse_results(file):

    filename = os.path.join("data", file)
    data = json.loads(open(filename, "r").read())
    lib_ranges = {}
    jdk_count = len(data.keys())

    for jdk in data:
        if "jdk1.8." in jdk:
            continue
        for dependency in data[jdk]:
            version_range = data[jdk][dependency]
            if not dependency in lib_ranges.keys():
                lib_ranges[dependency] = []
            lib_ranges[dependency].append(version_range)

    # print(f"-----{filename}-----\n")
    # print(f"jdk count: {jdk_count}")

    is_all_libs_common = True

    for dependency in lib_ranges:
        # print(dependency)
        common_libs = functools.reduce(np.intersect1d, (lib_ranges[dependency]))
        all_libs = functools.reduce(np.union1d, (lib_ranges[dependency]))
        # print(common_libs)

        if len(common_libs) != len(all_libs):
            is_all_libs_common = False
            break


    print(filename)

    file_obj = {}

    list_jdk = sorted(list(data.keys()), key=functools.cmp_to_key(jdk_sort_function))
    file_obj["_jdk"] = list_jdk

    print(len(list_jdk))

    if is_all_libs_common:
        for dependency in lib_ranges:
            print(dependency)
            common_libs = functools.reduce(np.intersect1d, (lib_ranges[dependency]))
            file_obj[dependency] = sorted(list(common_libs), key=functools.cmp_to_key(version_sort_function))
            print(file_obj[dependency])

        with open(os.path.join("results", "condensed", file), "w") as out_file:
            out_file.write(json.dumps(file_obj, indent=4))
    elif not is_all_libs_common:
        for dependency in lib_ranges:
            print(dependency)

            df = pd.DataFrame(flatten(lib_ranges[dependency]), columns=['version']).value_counts().reset_index(name='count')
            print(df.to_csv())
            df['count'] = df['count'].add(-1 * jdk_count).mul(-1)
            df = df[df['count'] <= 0.1 * jdk_count]
            file_obj[dependency] = df['version'].to_numpy().tolist()
            print(file_obj[dependency])

        with open(os.path.join("results", "culled_thresh_10_percent", file), "w") as out_file:
             out_file.write(json.dumps(file_obj, indent=4))



'''
    else:
        for dependency in lib_ranges:
            #print(dependency)
            common_libs = functools.reduce(np.intersect1d, (lib_ranges[dependency]))

            #file_obj[dependency] = sorted(list(common_libs), key=functools.cmp_to_key(version_sort_function))
            #print(file_obj[dependency])

            df = pd.DataFrame(flatten(lib_ranges[dependency]), columns=['version']).value_counts().reset_index(name='count')
            df['count'] = df['count'].add(-1 * jdk_count).mul(-1)
            df = df[df['count'] == 1]
            print(df)
'''


for file in os.listdir("data"):
    if os.path.isfile(f"data/{file}"):
        parse_results(file)

parse_results("Wicket1.json")
