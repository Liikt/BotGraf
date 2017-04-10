import requests
import sys
import yaml

file = open("config/secretary.yml", "r")
tmp = yaml.load(file)
file.close()
old_list = list(tmp.keys())
shiplist = ["Abukuma","Agano","Akashi","Akatsuki","Akigumo","Akitsu Maru","Akitsushima","Akizuki","Amagi","Amatsukaze","Aquila","Arashi","Asagumo","Asakaze","Ashigara","Ayanami","Bismarck","Chitose","Chiyoda","Commandant Teste","Fubuki","Graf Zeppelin","Hagikaze","Harukaze","Haruna","Haruna (fog)","Harusame","Hatsukaze","Hatsuzuki","Hayashimo","Hayasui","Hibiki","Hiei","Hiryuu","I-13","I-14","I-168","I-19","I-26","I-401","I-58","I-8","Iona (fog)","Iowa","Isokaze","Kaga","Kamikaze","Kashima","Katori","Katsuragi","Kawakaze","Kazagumo","Kinu","Kinugasa","Kirishima","Kitakami","Kiyoshimo","Kongou","Kumano","Libeccio","Littorio","Maikaze","Makigumo","Maruyu","Matsukaze","Mikuma","Minazuki","Mizuho","Mogami","Murakumo","Musashi","Myoukou","Naganami","Noshiro","Nowaki","Okinami","Ooi","Ooyodo","Oyashio","Pola","Prinz Eugen","Roma","Sakawa","Saratoga","Shigure","Shoukaku","Souryuu","Suzuya","Taigei","Taihou","Takanami","Takao (fog)","Teruzuki","Tokitsukaze","U-511","Umikaze","Unryuu","Uranami","Warspite","Yahagi","Yamagumo","Yamakaze","Yamato","Yuubari","Yuugumo","Z1","Z3","Zara","Zuihou","Zuikaku"]
for x in shiplist:
    re = requests.get("http://kancolle.wikia.com/wiki/" + x.replace(" ", "_"))
    if re.status_code == 200 and x not in old_list:
        html = re.text
        try:
            quotes_raw = html.replace("\n", "").split('<tr><th>Time</th><th>Japanese</th><th>English</th><th>Note</th></tr><tr>')[1].split("<td></td></tr></table>")[0].replace("</td>", "")
            all_list = quotes_raw.split("<td>")
            hourlies = [all_list[x] for x in range(len(all_list)) if (x+1)%4==0]
            file = open("config/secretary.yml", "r")
            secr = yaml.load(file)
            file.close()
            new = x.replace("_", " ")
            secr[new] = hourlies
            print(sorted(secr.keys()))
            file = open("config/secretary.yml", "w")
            yaml.dump(secr, file, default_flow_style=False)
            old_list.append(new)
        except Exception as e:
            print("I couldn't find any hourly notifications.")
            print(e)
    elif x in old_list:
        print("Already got", x, "Skipping!")
    else:
        print("I didn't find", x, "and got", re.status_code)