def file_format():
    file1 = open("input.txt")
    file2 = open("input2.txt")
    file3 = open("output.txt", "w")
    current_dic = {}
    for line in file1:
        line_split = line.split()
        repo = line_split[0].split("/")
        current_dic[repo[1]] = line_split[1]
    for line in file2:
        repo = line.strip()
        if repo in current_dic:
            file3.write(f"{repo}, Gradle, {current_dic.get(repo)}\n")
        else:
            file3.write(f"{repo}, Gradle, FALSE\n")


if __name__ == '__main__':
    print('This is a sample project with all the helpful tools implementations.')
    file_format()
