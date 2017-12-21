import GPUtil
import time
import os
import subprocess
import signal
import json
import hashlib


class RandomSearch:

    def __init__(self, executable, params, name=None, gpu=None):
        self.executable = executable
        self.params = params
        self.name = name
        self.gpu = gpu
        self.launched = []

    @property
    def keys(self):
        return sorted(list(self.params.keys()))

    def tune(self, n_jobs, out, wait_seconds=20):
        try:
            for i, (command, params) in enumerate(self.generate_jobs(n_jobs)):
                print('Running job {}/{}\n{}'.format(i+1, n_jobs, command))

                if self.name is not None:
                    name = params[self.name]
                else:
                    name = str(i)
                fout = open(os.path.join(out, '{}.out'.format(name)), 'w')
                ferr = open(os.path.join(out, '{}.err'.format(name)), 'w')
                p = subprocess.Popen(command, shell=True, stdout=fout, stderr=ferr, preexec_fn=os.setsid)
                with open(os.path.join(out, '{}.json'.format(name)), 'w') as f:
                    json.dump({
                        'params': params,
                        'command': command,
                        'pid': p.pid
                    }, f, indent=4)
                self.launched.append((p, fout, ferr))
                time.sleep(wait_seconds)
            for p, fout, ferr in self.launched:
                if p.poll() is None:
                    time.sleep(1)
        except Exception as e:
            print('killing {} jobs'.format(self.launched))
            for p, fout, ferr in self.launched:
                if p.poll() is None:  # it's still running
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                if not fout.closed:
                    fout.close()
                if not ferr.closed:
                    ferr.close()
            raise e

    def generate_jobs(self, n, wait_seconds=20):
        for i in range(n):
            params = {name: spec.sample() for name, spec in self.params.items()}
            if self.name is not None:
                ids = ['{}={}'.format(k, params[k]) for k in self.keys]
                params[self.name] = hashlib.sha256(','.join(ids).encode()).hexdigest()
            gpu_prefix = ''
            if self.gpu is not None:
                while True:
                    available = GPUtil.getAvailable(order='first', limit=1, maxMemory=0.01)
                    if available:
                        break
                    else:
                        time.sleep(wait_seconds)
                params['gpu'] = 0
                gpu_prefix = 'CUDA_VISIBLE_DEVICES={} '.format(available[0])
            command = '{}{} '.format(gpu_prefix, self.executable)
            specs = []
            for k in sorted(list(params.keys())):
                v = params[k]
                specs.append('--{} {}'.format(k, v))
            command += ' '.join(specs)
            yield command, params
