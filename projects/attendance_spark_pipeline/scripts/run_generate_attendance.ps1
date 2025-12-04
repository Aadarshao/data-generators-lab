# PowerShell helper to generate attendance data via CLI
param(
    [string]$OutPath = "..\..\data\raw\attendance_local.csv"
)

python -m data_generators generate attendance --out $OutPath
