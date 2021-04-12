import requests, os, subprocess
# try to start the server
try:
	os.chdir("Server-Dictionary")
	p = subprocess.Popen("start.bat")
	stdout, stderr = p.communicate()
# build the server
except:
	# confirm the eula
	if input("Do you agree to the eula at https://account.mojang.com/documents/minecraft_eula \n [Y/N]").lower() == "y":
		# create the main Dictionary
		p=subprocess.Popen("mkdir Server-Dictionary", shell=True)
		p.wait()
		os.chdir("Server-Dictionary")
		# Download link for the server
		file_url = ["https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar"]
		whatV = int(input("What server version? 1.16.5[0]\n"))
		# Download the server.jar
		r = requests.get(file_url[whatV], stream = True)
		with open("server.jar","wb") as data:
			for chunk in r.iter_content(chunk_size=1024):
				# writing one chunk at a time to file
				if chunk:
					data.write(chunk)
		# run server.jar
		subprocess.call(['java', '-jar', 'server.jar'])
		# override the eula
		with open("eula.txt", "w") as file:
			file.write("eula=TRUE")
		# create the batch file
		ram = input("How much gigabyte ram should have the server? exaple: 1 means 1 gigabyte ram\n")
		with open("start.bat", "w") as file:
			file.write(f"java -Xmx{ram}G -jar server.jar nogui")
		# edit server
		infile = open('server.properties','r+')
		content = infile.read()
		port = input('Change port ["port"/N]')
		if port.lower() != "n":
			table = str.maketrans("server-port=25565",f'server-port={port}')
		seed = input('Change seed ["seed"/N]')
		if seed.lower() != "n":
			table = str.maketrans("level-seed=",f'level-seed={seed}')
		gamemode = input('Change gamemode ["0/1/2/3"/N]')
		if gamemode.lower() != "n":
			if gamemode == 1:	gamemode = "creative"
			elif gamemode == 2: gamemode = "adventure"
			elif gamemode == 3: gamemode = "spectator"
			else: gamemode = "survival"
			table = str.maketrans("gamemode=survival",f'gamemode={gamemode}')
		name = input('What is the name of the server?\n')
		table = str.maketrans("motd=A Minecraft Server",f'motd={name}')
		content = content.translate(table)  #replaces 'foo' with 'bar'
		infile.write(content)
		infile.close()
		print("You can change settings at server.properties")
		# start server
		p = subprocess.Popen("start.bat")
		stdout, stderr = p.communicate()
