# server-based syntax
# ======================
# Defines a single server with a list of roles and multiple properties.
# You can define all roles on a single server, or split them:

# server "example.com", user: "deploy", roles: %w{app db web}, my_property: :my_value
# server "example.com", user: "deploy", roles: %w{app web}, other_property: :other_value
# server "db.example.com", user: "deploy", roles: %w{db}
server '128.8.164.178', user: 'deploy', roles: %w{app db web}

set :default_env, { 
  'DEVISE_SECRET_TOKEN' => 'd2043e35c7fc2d09d2dbb0433b60796c8663713abfcba67025b2176a704fc8d674e0ed79c7b1c9990d3808432ebc2205277364537f1c1870ce6fd69e8998bf63',
  'SECRET_KEY_BASE_TOKEN' => 'd2043e35c7fc2d09d2dbb0433b60796c8663713abfcba67025b2176a704fc8d674e0ed79c7b1c9990d3808432ebc2205277364537f1c1870ce6fd69e8998bf63',
  'SCRIBE_BOT_TOKEN' => '5acd09095472610fd1000000:Eh1JksCK8zs1_6RNU6CD',
  'FACEBOOK_ID' => '1689853631267050',
  'FACEBOOK_SECRET' => 'b9133c1bf4cbe47e153954b1d0d13a5f'
}


# role-based syntax
# ==================

# Defines a role with one or multiple servers. The primary server in each
# group is considered to be the first unless any hosts have the primary
# property set. Specify the username and a domain or IP for the server.
# Don't use `:all`, it's a meta role.

# role :app, %w{deploy@example.com}, my_property: :my_value
# role :web, %w{user1@primary.com user2@additional.com}, other_property: :other_value
# role :db,  %w{deploy@example.com}



# Configuration
# =============
# You can set any configuration variable like in config/deploy.rb
# These variables are then only loaded and set in this stage.
# For available Capistrano configuration variables see the documentation page.
# http://capistranorb.com/documentation/getting-started/configuration/
# Feel free to add new variables to customise your setup.



# Custom SSH Options
# ==================
# You may pass any option but keep in mind that net/ssh understands a
# limited set of options, consult the Net::SSH documentation.
# http://net-ssh.github.io/net-ssh/classes/Net/SSH.html#method-c-start
#
# Global options
# --------------
#  set :ssh_options, {
#    keys: %w(/home/rlisowski/.ssh/id_rsa),
#    forward_agent: false,
#    auth_methods: %w(password)
#  }
#
# The server-based syntax can be used to override options:
# ------------------------------------
# server "example.com",
#   user: "user_name",
#   roles: %w{web app},
#   ssh_options: {
#     user: "user_name", # overrides user setting above
#     keys: %w(/home/user_name/.ssh/id_rsa),
#     forward_agent: false,
#     auth_methods: %w(publickey password)
#     # password: "please use keys"
#   }
