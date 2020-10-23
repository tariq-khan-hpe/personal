$report_directory = ".\BOMs"

$merged_reports = @()

# Loop through each XLSX-file in $report_directory
foreach ($report in (Get-ChildItem "$report_directory\*.xlsx")) {

    # Loop through each row of the "current" XLSX-file
    $report_content = foreach ($row in Import-Excel $report -StartRow 5) {
        # Create "custom" row
        [PSCustomObject]@{
            "Building Block" = $report.Name
            "Qty"        = $row."Qty"
            "Product #"    = $row."Product #"
            "Product Description"    = $row."Product Description"
            "Mainstream"        = $row."Mainstream"
            "Shipment Lead Time"        = $row."Shipment Lead Time"
            "Unit Price (USD)"        = $row."Unit Price (USD)"
            "Extended List Price (USD)"        = $row."Extended List Price (USD)"
        }
    }

    # Add the "custom" data to the results-array
    $merged_reports += @($report_content)
}

# Create final report
$merged_reports | Export-Excel ".\merged_BOM.xlsx"