{{/*
Expand the name of the chart.
*/}}
{{- define "common.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Standard labels applied to all resources
*/}}
{{- define "common.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: pycrest
{{- end }}

{{/*
Selector labels — used in matchLabels and pod template labels
*/}}
{{- define "common.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
ServiceAccount name convention: <chart-name>-sa
*/}}
{{- define "common.serviceAccountName" -}}
{{ .Chart.Name }}-sa
{{- end }}

{{/*
Full image reference — respects global registry override
Usage: {{ include "common.image" . }}
*/}}
{{- define "common.image" -}}
{{- $registry := .Values.global.imageRegistry | default "" -}}
{{- $repo := .Values.image.repository -}}
{{- $tag := .Values.image.tag | default "latest" -}}
{{- if $registry -}}
{{ $registry }}/{{ $repo }}:{{ $tag }}
{{- else -}}
{{ $repo }}:{{ $tag }}
{{- end -}}
{{- end }}

{{/*
Inject both the global secret and the global configmap as envFrom sources.
All Python services and the Node gateway use this.
*/}}
{{- define "common.envFrom" -}}
- secretRef:
    name: pycrest-global-secret
- configMapRef:
    name: pycrest-global-config
{{- end }}

{{/*
VolumeMount for the shared NFS uploads PVC.
Add to containers[].volumeMounts for services that handle file uploads.
*/}}
{{- define "common.uploadsVolumeMount" -}}
- name: uploads
  mountPath: /app/uploads
{{- end }}

{{/*
Volume spec referencing the shared NFS uploads PVC.
Add to spec.volumes for services that handle file uploads.
*/}}
{{- define "common.uploadsVolume" -}}
- name: uploads
  persistentVolumeClaim:
    claimName: pycrest-uploads-pvc
{{- end }}

{{/*
Standard RollingUpdate strategy.
maxUnavailable: 1 means at most 1 pod down during update.
maxSurge: 1 means at most 1 extra pod spun up during update.
*/}}
{{- define "common.rollingUpdateStrategy" -}}
type: RollingUpdate
rollingUpdate:
  maxUnavailable: 1
  maxSurge: 1
{{- end }}

{{/*
Pod anti-affinity — prefer spreading pods across different nodes.
Pass the service name as the argument.
Usage: {{ include "common.podAntiAffinity" . }}
*/}}
{{- define "common.podAntiAffinity" -}}
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: {{ .Chart.Name }}
        topologyKey: kubernetes.io/hostname
{{- end }}



{{/*
Standard liveness probe on /health for Python uvicorn services (port 8000)
*/}}
{{- define "common.livenessProbe" -}}
httpGet:
  path: /health
  port: 8000
initialDelaySeconds: 20
periodSeconds: 30
timeoutSeconds: 5
failureThreshold: 3
{{- end }}

{{/*
Standard readiness probe on /health for Python uvicorn services (port 8000)
*/}}
{{- define "common.readinessProbe" -}}
httpGet:
  path: /health
  port: 8000
initialDelaySeconds: 10
periodSeconds: 10
timeoutSeconds: 5
failureThreshold: 3
{{- end }}

{{/*
minReadySeconds — how long a pod must be Ready before deployment counts it available.
Prevents sending traffic to pods that haven't fully warmed up.
Default: 10 seconds. Override per-service in values.yaml.
*/}}
