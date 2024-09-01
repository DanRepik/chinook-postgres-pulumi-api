# devtools.sh

# api operations
alias up="pulumilocal up --yes --stack local"
alias down="pulumilocal destroy --yes --stack local"

# import playground commands
source "${HOME}/workspace/localstack_playground/devtools.sh"

alias postgres_secret="install_secret --secret-name \"postgres/chinook\" \
  --engine postgres \
  --host postgres_db \
  --database chinook_auto_increment \
  --user chinook_user \
  --password chinook_password \
  --schema public"

# playground operations
alias infra_up="playground_postgres; postgres_secret"
alias infra_down="playground_down"
alias infra_reset="playground_reset"

