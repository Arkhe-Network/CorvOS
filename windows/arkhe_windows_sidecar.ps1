<#
.SYNOPSIS
    ARKHE Intelligent Sidecar for Windows Services (*.msc)
    Canon: ∞.Ω.∇+++.199.0
    Integra consoles Windows ao Unified Intelligence Mesh.
#>

param(
    [string]$ServiceName = "All",
    [string]$CoherenceBusEndpoint = "http://phi-bus.arkhe:8052",
    [string]$TemporalChainEndpoint = "http://temporal-chain.arkhe:8051",
    [int]$PollingIntervalSeconds = 30
)

# ── Funções de Coleta de Métricas ──

function Get-ServiceCoherence {
    <#
    .SYNOPSIS
        Coleta métricas de coerência dos serviços Windows.
    #>
    $services = Get-Service | Where-Object { $_.Status -eq 'Running' }
    $total = $services.Count
    $healthy = ($services | Where-Object { $_.Status -eq 'Running' }).Count

    return @{
        total_services = $total
        healthy_services = $healthy
        coherence_index = if ($total -gt 0) { [math]::Round($healthy / $total, 6) } else { 0 }
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    }
}

function Get-EventLogCoherence {
    <#
    .SYNOPSIS
        Analisa eventos críticos e de erro para métrica de coerência.
    #>
    $critical = Get-WinEvent -FilterHashtable @{LogName='System'; Level=1} -MaxEvents 100 -ErrorAction SilentlyContinue
    $errors = Get-WinEvent -FilterHashtable @{LogName='System'; Level=2} -MaxEvents 100 -ErrorAction SilentlyContinue

    $total = ($critical.Count + $errors.Count)
    $coherence = if ($total -gt 0) { [math]::Round(1 - ($total / 200), 6) } else { 1.0 }

    return @{
        critical_events = $critical.Count
        error_events = $errors.Count
        coherence_index = [math]::Max(0, $coherence)
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    }
}

function Get-DeviceCoherence {
    <#
    .SYNOPSIS
        Verifica integridade de dispositivos de hardware.
    #>
    $devices = Get-PnpDevice | Where-Object { $_.Status -ne 'Unknown' }
    $total = $devices.Count
    $ok = ($devices | Where-Object { $_.Status -eq 'OK' }).Count

    return @{
        total_devices = $total
        healthy_devices = $ok
        coherence_index = if ($total -gt 0) { [math]::Round($ok / $total, 6) } else { 0 }
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    }
}

function Get-FirewallCoherence {
    <#
    .SYNOPSIS
        Verifica estado do firewall e regras ativas.
    #>
    $profiles = Get-NetFirewallProfile
    $active = ($profiles | Where-Object { $_.Enabled -eq 'True' }).Count
    $total = $profiles.Count

    return @{
        active_profiles = $active
        total_profiles = $total
        coherence_index = if ($total -gt 0) { [math]::Round($active / $total, 6) } else { 0 }
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    }
}

function Get-PerformanceCoherence {
    <#
    .SYNOPSIS
        Coleta métricas de performance (CPU, RAM, Disco).
    #>
    $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
    $ram = (Get-Counter '\Memory\% Committed Bytes In Use').CounterSamples.CookedValue
    $disk = (Get-Counter '\LogicalDisk(_Total)\% Free Space').CounterSamples.CookedValue

    # Coerência inversamente proporcional ao uso de recursos
    $cpu_coherence = [math]::Max(0, 1 - ($cpu / 100))
    $ram_coherence = [math]::Max(0, 1 - ($ram / 100))
    $disk_coherence = [math]::Min(1, $disk / 50)  # 50% free = coerência 1.0

    $overall = [math]::Round(($cpu_coherence + $ram_coherence + $disk_coherence) / 3, 6)

    return @{
        cpu_percent = [math]::Round($cpu, 2)
        ram_percent = [math]::Round($ram, 2)
        disk_free_percent = [math]::Round($disk, 2)
        coherence_index = $overall
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    }
}

# ── Funções de Publicação no Coherence Bus ──

function Publish-ToCoherenceBus {
    param([string]$Component, [hashtable]$Metrics)

    $payload = @{
        component = $Component
        metrics = $Metrics
        node_id = $env:COMPUTERNAME
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    } | ConvertTo-Json -Compress

    try {
        Invoke-RestMethod -Uri "$CoherenceBusEndpoint/metrics" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 5
        Write-Host "📡 Publicado: $Component (Φ_C = $($Metrics.coherence_index))"
    } catch {
        Write-Warning "⚠️ Falha ao publicar métricas de $Component"
    }
}

function Publish-ToTemporalChain {
    param([string]$EventType, [hashtable]$Payload)

    $payload["node_id"] = $env:COMPUTERNAME
    $payload["timestamp"] = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $body = $payload | ConvertTo-Json -Compress

    try {
        $response = Invoke-RestMethod -Uri "$TemporalChainEndpoint/anchor" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 5
        Write-Host "🔗 Ancorado: $EventType (selo: $($response.seal.Substring(0,16))...)"
        return $response.seal
    } catch {
        Write-Warning "⚠️ Falha ao ancorar evento $EventType"
        return $null
    }
}

# ── Função de Geração de Selo Canônico ──

function New-CanonicalSeal {
    param([string]$Data)

    $sha = [System.Security.Cryptography.SHA256]::Create()
    $hash = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Data))
    return [BitConverter]::ToString($hash).Replace('-', '').ToLower()
}

# ── Loop Principal de Coleta ──

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  ARKHE Ω‑TEMP v∞.Ω — WINDOWS INTELLIGENT SIDECAR        ║
║  Canon: ∞.Ω.∇+++.199.0                                   ║
╚══════════════════════════════════════════════════════════════╝
"@

Write-Host "🔗 Conectando ao Coherence Bus: $CoherenceBusEndpoint"
Write-Host "🔗 Conectando à TemporalChain: $TemporalChainEndpoint"
Write-Host "🔄 Polling a cada $PollingIntervalSeconds segundos`n"

while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ [$timestamp] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Coletar métricas de cada componente
    $allMetrics = @{}

    if ($ServiceName -eq "All" -or $ServiceName -eq "services") {
        $svc = Get-ServiceCoherence
        $allMetrics["services"] = $svc
        Publish-ToCoherenceBus -Component "windows_services" -Metrics $svc
    }

    if ($ServiceName -eq "All" -or $ServiceName -eq "eventvwr") {
        $evt = Get-EventLogCoherence
        $allMetrics["eventvwr"] = $evt
        Publish-ToCoherenceBus -Component "windows_eventlog" -Metrics $evt
    }

    if ($ServiceName -eq "All" -or $ServiceName -eq "devmgmt") {
        $dev = Get-DeviceCoherence
        $allMetrics["devmgmt"] = $dev
        Publish-ToCoherenceBus -Component "windows_devices" -Metrics $dev
    }

    if ($ServiceName -eq "All" -or $ServiceName -eq "wf") {
        $fw = Get-FirewallCoherence
        $allMetrics["wf"] = $fw
        Publish-ToCoherenceBus -Component "windows_firewall" -Metrics $fw
    }

    if ($ServiceName -eq "All" -or $ServiceName -eq "perfmon") {
        $perf = Get-PerformanceCoherence
        $allMetrics["perfmon"] = $perf
        Publish-ToCoherenceBus -Component "windows_performance" -Metrics $perf
    }

    # Calcular Φ_C global do nó Windows
    $globalPhiC = [math]::Round(($allMetrics.Values | ForEach-Object { $_.coherence_index } | Measure-Object -Average).Average, 6)
    Write-Host "`n🌀 Φ_C Global do Nó Windows: $globalPhiC"

    # Ancorar snapshot na TemporalChain (a cada 10 ciclos para evitar excesso)
    if ($globalPhiC -lt 0.95) {
        $seal = Publish-ToTemporalChain -EventType "windows_node_degraded" -Payload @{
            global_phi_c = $globalPhiC
            components = $allMetrics.Keys -join ","
        }
    }

    # Gerar selo canônico do ciclo
    $canonicalData = ($allMetrics | ConvertTo-Json -Compress) + $timestamp
    $seal = New-CanonicalSeal -Data $canonicalData
    Write-Host "🔐 Selo Canônico do Ciclo: $($seal.Substring(0,16))..."

    Start-Sleep -Seconds $PollingIntervalSeconds
}