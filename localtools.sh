alias up="pulumilocal up --yes --stack local"
alias down="pulumilocal destroy --yes --stack local"

# import playground commands
source "${HOME}/workspace/localstack_playground/devtools.sh"

alias infra_up="playground_postgres; ./install_secrets.py"
alias infra_down="playground_down"
alias infra_reset="playground_reset"

