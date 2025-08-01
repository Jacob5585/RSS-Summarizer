function colorizeLog(logText) {
    let coloredLog = logText;

    // Colorize timestamps
    coloredLog = coloredLog.replace(/(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}-\d{6})/g, '<span class="timestamp">$1</span>');

    // Colorize file paths
    coloredLog = coloredLog.replace(/(\.\.\/[^\s]+(\.mp3|\.txt|\.log|\.json|\.py|\.js|\.html))/g, '<span class="filepath">$1</span>');

    // Colorize INFO, WARNING, ERROR
    coloredLog = coloredLog.replace(/INFO/g, '<span class="info">INFO</span>');
    coloredLog = coloredLog.replace(/WARNING/g, '<span class="warning">WARNING</span>');
    coloredLog = coloredLog.replace(/ERROR/g, '<span class="error">ERROR</span>');

    return coloredLog;
}