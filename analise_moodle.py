from datetime import datetime

class Moodle:

    MEMBROS_EQUIPE = ["ifarraguirre@gmail.com",
                  "rosa.tiago@pucrs.br",
                  "alleff.deus@pucrs.br",
                  "neverson.silva@pucrs.br",
                  "franz.silva@pucrs.br",
                  "vitoria.souza@pucrs.br",
                  "sophia.mendes@edu.pucrs.br",
                  "rafael.chanin@pucrs.br",
                  "educacao.continuada@pucrs.br",
                  "p.pasinato@edu.pucrs.br",
                  "dharana.rivas@eldorado.org.br",
                  "nicolas.nascimento@acad.pucrs.br",
                  "npn.adsl@gmail.com",
                  "lipepereira2003@gmail.com",
                  "filipe.pereira002@edu.pucrs.br",
                  "branda.weppo@pucrs.br",
                  "https://ticemtrilhas.instructure.com/users/27093",
                  "Student",
                  "gizele.analista@gmail.com",
                  "https://ticemtrilhas.instructure.com/users/27266",
                  "https://ticemtrilhas.instructure.com/users/21555",
                  "https://ticemtrilhas.instructure.com/users/21627",
                  "https://ticemtrilhas.instructure.com/users/10677",
                  "https://ticemtrilhas.instructure.com/users/29558",
                  "https://ticemtrilhas.instructure.com/users/3157",
                  "980c7cdde96665e6ea8f2234a4af84b308ca0fd3",
                  "leonardo.oliveira@pucrs.br",
                  "sassiarts@outlook.com",
                  "cristiano.clezar@pucrs.br",
                  "teste@teste.com",
                  "ivoneimarques@gmail.com",
                  "leonardoko@gmail.com",
                  "franzfigueroa@gmail.com",
                  "ivonei.marques@pucrs.br",
                  "rafael.chanin@gmail.com",
                  "suportessi2023@gmail.com",
                  "sassiarts@outlook.com"]

    MESES = {
        "jan": 1,
        "fev": 2,
        "mar": 3,
        "abr": 4,
        "mai": 5,
        "jun": 6,
        "jul": 7,
        "ago": 8,
        "set": 9,
        "out": 10,
        "nov": 11,
        "dez": 12
    }

    def __init__(self):
        print("Moodle class initialized")
        self.len_modules_moodle = 0
        self.names_modules_moodle = []

    def retira_membros_equipe(self, email):
        '''Função para verificação de membros da equipe que não devem estar nos números indicadores da trilha'''
        if email in self.MEMBROS_EQUIPE:
            return False
        return True
    
    def count_modules_moodle(self, data):
        '''Função para contagem dos módulos da trilha do moodle'''
        count = 0
        name_modules = []
        for x in data[4:]:
            if "Último download realizado neste curso." not in x:
                if "Total do curso" not in x:
                    count += 1
                    if "\xa0" in x:
                        name_modules.append(x.split("Questionário:")[1].replace("\xa0","").split(" (")[0])
                    else:
                        name_modules.append(x.split("Questionário:")[1].split(" (")[0])
            else:
                break
        self.len_modules_moodle = count
        self.names_modules_moodle = name_modules
        return count, name_modules

    def sort_data_moodle(self, content):
        '''Função que gerencia os dados do arquivo de datas do moodle'''
        combined_row = []
        aux_header = content[0]
        header = ["Nome Completo","Email",*aux_header[3:]]
        
        for row in content[1:]:
            combined_row.append([row[0] + " " + row[1], *row[2:]]) 
        combined_row = sorted(combined_row, key=lambda x: x[0])
        
        content_to_return = [header, *combined_row]
        return content_to_return

    def read_moodle_datas(self, file_datas, data_readed):
        # '''Função para a leitura das informações de datas das atividades do moodle'''
        
        data = []
        data_readed_notas = []
        for x in file_datas:
            data.append(x)
        count = 0
        data[0].insert(0, "Hora")
        for row in data[1:]:
            if self.retira_membros_equipe(row[2]):
                data_aux1 = row[0].split(", ")
                row.insert(0, data_aux1[2])
                data_aux2 = data_aux1[1].split(" ")
                data_aux3 = f"{data_aux2[0]}-{self.MESES[data_aux2[1].split(".")[0]]}-{data_aux2[2]}"
                row[1] = data_aux3
                data_readed_notas.append(row)
                count += 1

        for x in data_readed_notas:
            if "Total do curso" in x:
                data_readed_notas.remove(x)

        data[0][1] = "Data"

        limpo = []
        student_email = ''
        count_notfound = 0
        no_se = []
        
        no_se.append(data[0])
        for x in data_readed[1:]:
            aux = []
            for y in data_readed_notas:
                if x[1] == y[3]:
                    aux.append(y)
            unique_entries = {}
            for entry in aux:
                module_name = entry[4]
                student_email = entry[3]
                entry[6] = entry[6].replace(',','.')
                if student_email not in unique_entries:
                    unique_entries[student_email] = {}
                    if module_name not in unique_entries[student_email]:
                        unique_entries[student_email][module_name] = entry
                    else:
                        if entry[6] != '':
                            if float(entry[6]) > float(unique_entries[student_email][module_name][6]):
                                unique_entries[student_email][module_name] = entry
                else:
                    if module_name not in unique_entries[student_email]:
                        unique_entries[student_email][module_name] = entry
                    else:
                        if entry[6] != '':
                            # Convertendo os campos de data e hora para objetos datetime
                            data_hora_atual = datetime.strptime(unique_entries[student_email][module_name][1] + " " + unique_entries[student_email][module_name][0], "%d-%m-%Y %H:%M")
                            data_hora_nova = datetime.strptime(entry[1] + " " + entry[0], "%d-%m-%Y %H:%M")

                            # Verificando qual das entradas é a mais antiga
                            if data_hora_nova < data_hora_atual:
                                if float(unique_entries[student_email][module_name][6]) < 7.00 and float(entry[6]) >= 7.00:
                                    unique_entries[student_email][module_name] = entry
                                elif float(unique_entries[student_email][module_name][6]) >= 7.00 and float(entry[6]) >= 7.00:
                                    unique_entries[student_email][module_name] = entry
                            else:
                                if float(unique_entries[student_email][module_name][6]) >= 7.00 and float(entry[6]) >= 7.00:
                                    unique_entries[student_email][module_name] = entry
                                elif float(entry[6]) >= 7.00 and float(unique_entries[student_email][module_name][6]) < 7.00:
                                    unique_entries[student_email][module_name] = entry
            if aux != []:
                for module_name, module_data in unique_entries[student_email].items():
                    limpo.append(module_data[1:])
            else:
                no_se.append(x)
                count_notfound += 1

        clean = []
        clean.append(data[0][1:])
        for row in limpo:
            clean.append(row)
        return clean, no_se

    def le_dados_notas(self, prefixo, content):
        '''Função para leitura dos dados de notas do moodle'''

        aux_notas = []
        count = 0

        for row in content:
            if count == 0:
                self.count_modules_moodle(row)
                count += 1
            if self.retira_membros_equipe(row[3]):
                aux_notas.append(row[1:])
                count += 1

        content = aux_notas
        return content
    
    def encontra_pessoas(self, filename_notas, filename_datas):

        '''Função para a junção das informações dos alunos (informações pessoais, datas das atividades e nota das atividades)'''
        final_data = []
        header = ["Nome Completo", "Email"]
        info_aux = {}
        for x in self.names_modules_moodle:
            header.append(x.replace("0",""))
            info_aux[x.replace("0","")] = ""
            header.append(f"Data|{x.replace("0","")}")
            info_aux[f"Data|{x.replace("0","")}"] = ""
            header.append(f"Status|{x.replace("0","")}")
            info_aux[f"Status|{x.replace("0","")}"] = ""
        final_data.append(header)

        for row_notas in filename_notas[1:]:
            info = {
                "Nome": "",
                "Email": ""
            }
            info.update(info_aux)
            for row_datas in filename_datas[1:]:
                if row_notas[1] == row_datas[2]:
                    if row_datas[1] not in info["Nome"]:
                        info["Nome"] = row_datas[1]
                        info["Email"] = row_datas[2]
                        nome_mod = row_datas[3].replace("0","")
                        if info.get(nome_mod, "") == "":
                            if row_datas[5] != "":
                                if float(row_datas[5]) >= 7.0:
                                    info[nome_mod] = row_datas[5]
                                    aux = "Status|"+nome_mod
                                    info[aux] = "Complete"
                                else:
                                    info[nome_mod] = row_datas[5]
                                    aux = "Status|"+nome_mod
                                    info[aux] = "Incomplete"
                            else:
                                aux = "Status|"+nome_mod
                                info[aux] = "Incomplete"
                        aux = "Data|"+nome_mod
                        if info.get(aux, "") == "":
                            if row_datas[5] != "":
                                info[aux] = row_datas[0]
                            else:
                                info[aux] = ""
                        
                    else:
                        nome_mod = row_datas[3].replace("0","")
                        if info.get(nome_mod, "") == "":
                            if row_datas[5] != "":
                                if float(row_datas[5]) >= 7.0:
                                    info[nome_mod] = row_datas[5]
                                    aux = "Status|"+nome_mod
                                    info[aux] = "Complete"
                                else:
                                    info[nome_mod] = row_datas[5]
                                    aux = "Status|"+nome_mod
                                    info[aux] = "Incomplete"
                            else:
                                aux = "Status|"+nome_mod
                                info[aux] = "Incomplete"
                        aux = "Data|"+nome_mod
                        if info.get(aux, "") == "":
                            if row_datas[5] != "":
                                info[aux] = row_datas[0]
                            else:
                                info[aux] = ""
                        
            if not all(value == "" for key, value in info.items()):
                final_data.append(list(info.values()))
        return final_data
    
    def junta_relatorio_parceiro(self, lostfile, final):
        '''Função que junta os relatórios de parceiros em um único arquivo'''
        lista_lost = []
        lista_final = []
        tam_header = 3 * self.len_modules_moodle
        for row in lostfile[1:]:
            nome_completo = row[0] + "*"
            lista_lost.append([nome_completo, row[1], row[2]] + [""] * tam_header)
        
        header = final[0]
        for x in lista_lost:
            lista_final.append(x)
        for row in final[1:]:
            lista_final.append(row)
        final_ordenado = sorted(lista_final, key=lambda x: x[0].lower())
        final_ordenado.insert(0,header)
        return final_ordenado
    
    def arquivo_metricas(self, data):
        '''Função que cria o arquivo de métricas do moodle'''
        metricas_copy = {
            "Total":0,
            "Concluintes":0,
            "Incompletos":0,
            "Nao_iniciados":0
        }

        metricas = {"metricas": metricas_copy}

        for row in data[1:]:
            metricas["metricas"]["Total"] += 1
            last_module = len(row) - 1

            status = row[last_module]
            if status == "Complete":
                metricas["metricas"]["Concluintes"] += 1
            elif status == "Incomplete":
                metricas["metricas"]["Incompletos"] += 1
            
            if "*" in row[0]:
                metricas["metricas"]["Nao_iniciados"] += 1
        
        return metricas