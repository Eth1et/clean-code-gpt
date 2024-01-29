import subprocess


def main():
    subprocess.run([
        'docker', 'run', '-d',
        '--name', 'sonarqube', 
        '-e', 'SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true', 
        '-p', '9000:9000', 
        'sonarqube:lts-community'
    ])


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
