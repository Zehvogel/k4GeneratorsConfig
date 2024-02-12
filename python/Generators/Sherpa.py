import os, stat
import SherpaProcDB

class Sherpa:
	"""Sherpa class"""
	def __init__(self, procinfo, settings):
		self.name = "Sherpa"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.ext = "dat"
		self.file = ""
		self.outdir = f"{procinfo.get('OutDir')}/Sherpa"
		self.outfileName = f"Run_{self.procinfo.get('procname')}.{self.ext}"
		self.outfile = f"{self.outdir}/{self.outfileName}"
		self.procDB = SherpaProcDB.SherpaProcDB(self.procinfo)
		self.procDB.write_DBInfo()

		self.executable  = "Sherpa -f"
		self.key4hepfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}.sh"
		self.gen_settings = settings.get_block("sherpa")
		if self.gen_settings is not None:
			self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

	def write_run(self):
		self.run = "(run){\n"

		self.add_run_option("RANDOM_SEED", self.procinfo.get_rndmSeed())

		ENG = self.procinfo.get("sqrts") / 2.
		beam1_pdg = self.procinfo.get_beam_flavour(1)
		beam2_pdg = self.procinfo.get_beam_flavour(2)

		self.add_run_option("BEAM_1", beam1_pdg)
		self.add_run_option("BEAM_2", beam2_pdg)

		self.add_run_option("BEAM_ENERGY_1", ENG)
		self.add_run_option("BEAM_ENERGY_2", ENG)
		self.add_run_option("MODEL", self.procinfo.get("model"))

		if self.procinfo.get("isr_mode"):
			self.add_run_option("PDF_LIBRARY", "PDFESherpa")
		else:
			self.add_run_option("PDF_LIBRARY", "None")
		self.add_run_option("EVENTS", self.procinfo.get("events"))
		self.run += "\n\n"
		for p in self.procinfo.get_data_particles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = self.is_sherpa_particle_data(attr)
					if name is not None:
						value = getattr(p, attr)
						op_name = f"{name}[{p.get('pdg_code')}]"
						self.add_run_option(op_name, value)
						
		if  self.procinfo.get("output_format") == "hepmc":
			eoutname="HepMC_GenEvent[{0}]".format(self.procinfo.get("procname"))
			self.add_run_option("EVENT_OUTPUT", eoutname)
			
		elif self.procinfo.get("output_format") == "hepmc3":
			eoutname="HepMC3_GenEvent[{0}]".format(self.procinfo.get("procname"))
			self.add_run_option("EVENT_OUTPUT", eoutname)
		self.run += self.procDB.get_run_out()
		if self.gen_settings is not None:
			if "run" in self.gen_settings.keys():
				for key,value in self.gen_settings["run"].items():
					self.add_run_option(key, value)



	def write_process(self):
		self.ptext = "(processes){\n"
		if self.procinfo.get("decay"):
			self.add_decay()
		else:
			self.ptext += f"  Process {self.procinfo.get_initial_pdg()} -> {self.procinfo.get_final_pdg()};\n"
		self.ptext += f"  Order ({self.procinfo.get_qcd_order()},{self.procinfo.get_qed_order()});\n"
		self.ptext += "  End process;\n"

	def add_decay(self):
		# Simple check first that parents are 
		# in the main process
		decay_opt = self.procinfo.get("decay")
		for key in decay_opt:
			if str(key) not in self.procinfo.get_final_pdg():
				print("Particle {0} not found in main process. Decay not allowed".format(key))
		# Sherpa requires the decaying particles get an additional label 25-> 25[a]
		# so parse letters to the process definition
		i = 97
		fs=""
		decays=""
		for p in self.procinfo.get_final_pdg_list():
			parent = str(p) + f"[{chr(i)}] "
			child = decay_opt[p]
			fs += parent
			decays += f"  Decay {parent} -> "
			for c in child: 
				decays += f"{c} "
			decays+="\n"  
			i+=1
		self.ptext += f"  Process {self.procinfo.get_initial_pdg()} -> {fs};\n"
		self.ptext += decays

		

	def write_file(self):
		self.write_run()
		self.write_process()
		self.ptext += "}(processes)\n\n"
		self.run += "}(run)\n\n"
		self.file = self.run + self.ptext
		with open(self.outfile, "w+") as file:
			file.write(self.file)

	def write_key4hepfile(self,shell,config):
		key4hepRun = shell+"\n"
		key4hepRun += config+"\n"
		key4hepRun += self.executable+" "+self.outfileName+"\n"
		key4hepRun += f"$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc2 -o edm4hep {self.procinfo.get('procname')}.hepmc2g {self.procinfo.get('procname')}.edm4hep\n"
		with open(self.key4hepfile, "w+") as file:
			file.write(key4hepRun)
		os.chmod(self.key4hepfile, os.stat(self.key4hepfile).st_mode | stat.S_IEXEC)

	def add_run_option(self, key, value):
		if self.gen_settings is not None:
			if "run" in self.gen_settings.keys():
				if key in self.gen_settings["run"]:
					value = self.gen_settings["run"][key]
		if key in self.run:
			if value in self.run:
				return
			print(f"{key} has already been defined in {self.name} with value.")
			return
		self.run += f" {key} {value};\n"

	def add_process_option(self, key, value):
		if key in self.ptext:
			print(f"{key} has already been defined in {self.name}.")
			return
		self.ptext += f" {key} {value};\n"

	def is_sherpa_particle_data(self, d):
		name = None
		if d == "mass":
			name = "MASS"
		if d == "width":
			name = "WIDTH"
		return name