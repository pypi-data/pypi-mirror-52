: ${HEALTHCHECK_CURL_MAX_TIME:=10}
: ${HEALTHCHECK_CURL_USER_AGENT:=curl-healthcheck}
: ${HEALTHCHECK_CURL_WRITE_OUT:='\n%{http_code} %{remote_ip}:%{remote_port} %{time_total} seconds\n'}

healthcheck_curl () {
  export NSS_SDB_USE_CACHE=no
  curl -g -k -q --fail \
    --max-time "${HEALTHCHECK_CURL_MAX_TIME}" \
    --user-agent "${HEALTHCHECK_CURL_USER_AGENT}" \
    --write-out "${HEALTHCHECK_CURL_WRITE_OUT}" \
    "$@" || return 1
}

healthcheck_port () {
  process=$1

  # ss truncate command name to 15 characters and this behaviour
  # cannot be diabled
  if [ ${#process} -gt 15 ] ; then
    process=${process:0:15}
  fi

  shift 1
  args=$@
  ports=${args// /|}
  ss -ntp | awk '{print $5,"-",$6}' | egrep ":($ports)" | grep "$process"
}

healthcheck_listen () {
  process=$1

  # ss truncate command name to 15 characters and this behaviour
  # cannot be diabled
  if [ ${#process} -gt 15 ] ; then
    process=${process:0:15}
  fi

  shift 1
  args=$@
  ports=${args// /|}
  ss -lnp | awk '{print $5,"-",$7}' | egrep ":($ports)" | grep "$process"
}

get_config_val () {
  crudini --get "$1" "$2" "$3" 2> /dev/null || echo "$4"
}

# apachectl -S is slightly harder to parse and doesn't say if the vhost is serving SSL
get_url_from_vhost () {
  vhost_file=$1
  server_name=$(awk '/ServerName/ {print $2}' $vhost_file)
  ssl_enabled=$(awk '/SSLEngine/ {print $2}' $vhost_file)
  bind_port=$(grep -h "<VirtualHost .*>" $vhost_file | sed 's/<VirtualHost .*:\(.*\)>/\1/')
  wsgi_alias=$(awk '/WSGIScriptAlias/ {print $2}' $vhost_file)
  proto=http
  if [[ $ssl_enabled == "on" ]]; then
    proto=https
  fi
  if [[ $wsgi_alias != "/" ]]; then
    wsgi_alias="${wsgi_alias}/"
  fi
  echo ${proto}://${server_name}:${bind_port}${wsgi_alias}
}
