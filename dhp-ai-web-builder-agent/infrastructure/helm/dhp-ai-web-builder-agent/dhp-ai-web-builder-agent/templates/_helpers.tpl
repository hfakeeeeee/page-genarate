{{- define "app_deploy.vars.secretProviderClassName" -}}
secretprovider-{{ .Values.appName }}
{{- end -}}

{{- define "app_deploy.vars.secretName" -}}
secret-{{ .Values.appName }}
{{- end -}}

{{- define "app_deploy.vars.configMapName" -}}
config-map-{{ .Values.appName }}
{{- end -}}

{{- define "app_deploy.vars.userAssignedIdentityID" -}}
{{ .Values.keyVault.userAssignedIdentityID }}
{{- end -}}

{{- define "app_deploy.vars.keyVault" -}}
{{ .Values.keyVault.name }}
{{- end -}}
