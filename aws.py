import parser 

def getCredentialsCommand(dir_path):
    args = parser.getArgs()
    return [f'aws-vault exec {args.env} --duration={args.duration_time}h -- env | grep --color=never ^AWS_ > {dir_path}']