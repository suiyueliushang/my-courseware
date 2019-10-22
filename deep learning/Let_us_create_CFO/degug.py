filecsv = join('label', str(self.id) + '.csv')
            if not os.path.exists(filecsv):
                with open(filecsv, 'w', encoding="utf-8") as f:
                    f.write('id, video name, video class, description\n')

            with open(filecsv) as file:
                reader = csv.reader(file)
                original =list(reader)
                print("original")
                print(original)
            os.remove(filecsv)

            with open(join('label', str(self.id) + '.csv'), 'w', encoding="utf-8",newline="") as f1:
                reader2 = csv.reader(f1)
                cc =list(reader2)
                print("cc")
                print(cc)
                content = csv.writer(f1)
                for row in original:
                    if '1024' not in row:
                        content.writerow(row)
                for i in range(len(self.file_list)):
                    content.writerow([self.info_str[i, 0], self.info_str[i, 1],self.info_str[i, 2],self.info_str[i, 3]])