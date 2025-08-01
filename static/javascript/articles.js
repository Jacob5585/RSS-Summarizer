let playbackSpeed = 2; // Default playback speed

function showSummary(id, summary, audioFile, category) {
    console.log("Summary ID:", id); // Debugging line
    console.log("Summary Content:", summary); // Debugging line
    // Set the summary content
    document.getElementById('summaryContent').innerText = summary;

    // Pause the audio if it's currently playing
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.pause(); // Stop the current audio
    audioPlayer.currentTime = 0; // Reset the audio to the beginning

    // Set the audio source
    const audioPath = `/audio/${category}/${audioFile}`;
    document.getElementById('audioSource').src = audioPath;
    audioPlayer.load(); // Load the new audio source

    // Display the summary popup
    document.getElementById('summaryPopup').style.display = 'block';
}

function closeSummary() {
    // Hide the summary popup
    document.getElementById('summaryPopup').style.display = 'none';
    // Pause the audio when closing the popup
    document.getElementById('audioPlayer').pause();
}

function playAudio() {
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.playbackRate = playbackSpeed; // Set playback speed
    audioPlayer.load(); // Load the new audio source
    audioPlayer.play(); // Play the audio
}

function setPlaybackSpeed(speed) {
    playbackSpeed = speed; // Update playback speed
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.playbackRate = playbackSpeed; // Set the new playback speed
}