# dynmat-assn

A repo for scripts made for the Dynamic behaviour of Materials final Project. Abaqus CAE 2024 required for running the 
geometry generation, Abaqus 2023 or newer for running the input files.

| File Name                 | Description                                                                               |
|---------------------------|-------------------------------------------------------------------------------------------|
| `abq_full_model.py`       | Script to be run in Abaqus CAE to generate geometry, boundary conditions, job, etc.       |
| `abq_script_model.py`     | Copy of `abq_full_model.py` but without parameters at the start.                          |
| `local_job_gen.py`        | Script to iterate through parameters and create `.inp` files using `abq_script_model.py`. |
| `job_gen_log.txt`         | Log file with the names of all the generated jobs.                                        |
| `euler_job_submission.py` | Script that loads all the jobs into the queue on euler.                                   |
| `euler_job_status.py`     | Script that reads the `.sta` files of the jobs.                                           |
| `euler_odb_extract.py`    | Script that extracts pictures and CSV files from ODB Databases.                           |
| `local_plots_from_csv.py` | Script that generates plots from CSV files on euler.                                      |
| `euler_sendToBox.py`      | Script that sends files straight to the storage box through ssh.                          |
| `euler_pullFromBox.py`    | Script that sends files straight from the storage box to euler through ssh.               |
| `dataExtractionConv.m`    | Reads file names and CSVs and stores them in a struct, then saves the struct.             |
| `rigidIndenterStudy.m`    | Opens the struct and compares results for different IDVs.                                 |
| `EPTStudy.m`              | Opens the struct and compares results for different EPTs.                                 |






### Usage of scripts:
- Set working directory and other parameters in `abq_script_model.py`
- Decide what parameters you want to iterate trough and which ones are fixed in `local_job_gen.py`
- Run `local_job_gen.py` (about 10 seconds per input file generated)
- Check `job_gen_log.txt` to make sure everything was generated
- Copy `.inp` files to euler cluster (or any machine with SLURM queue management)
- Load abaqus module on euler
- Run `euler_job_submission.py` to submit all the `.inp` files that have a certain naming scheme, check generated log
- Check queue state with `squeue`
- Check status files by running `euler_job_status.py` on euler
- After sims are done, run `euler_odb_extraction` with abaqus CAE then copy those new files back to local machine
- Optionally run `euler_sendToBox.py` to send files matching some naming scheme straight to the storage box
- Optionally run `local_plots_from_csv.py` to create some quick graphs out of the newly generated `.csv` files

Useful euler commands and things to know:
```
navigate to /cluster/scratch/yourKurzel
module load abaqus/2023
python3 --version
python3 euler_job_submission.py
sbatch -n 4 -t 1-0 --mem-per-cpu 4G --wrap "abaqus job=Job-1 double cpus=4 scratch=\$TMPDIR"
squeue
scancel <job_ID>
scancel --state=PENDING
scontrol show jobid –dd <job_ID>
python3 euler_job_status.py
abaqus cae noGUI=euler_odb_extract.py

```
