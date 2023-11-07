
document.addEventListener("DOMContentLoaded", function() 
{
    const sleepForm = document.getElementById("sleep-form");
    const sleepResults = document.getElementById("sleep-results");
    const sleepDurationText = document.getElementById("sleep-duration");
    const sleepCycleText = document.getElementById("sleep-cycle");
    const trackButton = document.getElementById("track-button");
    const sleepCycleInfoText = document.getElementById("sleep-cycle-info"); 

    function calculateSleepDuration(sleepTime, wakeTime) {
    const sleepTimeParts = sleepTime.split(":");
    const wakeTimeParts = wakeTime.split(":");

    let sleepHours = parseInt(sleepTimeParts[0]);
    const sleepMinutes = parseInt(sleepTimeParts[1]);
    let wakeHours = parseInt(wakeTimeParts[0]);
    const wakeMinutes = parseInt(wakeTimeParts[1]);

    if (sleepHours > wakeHours || (sleepHours === wakeHours && sleepMinutes > wakeMinutes)) {
        wakeHours += 24;
    }

    const totalSleepMinutes = (wakeHours - sleepHours) * 60 + (wakeMinutes - sleepMinutes);
    const hours = Math.floor(totalSleepMinutes / 60);
    const minutes = totalSleepMinutes % 60;

    return { hours, minutes };
    }

    function calculateSleepCycle(sleepHours, sleepMinutes) {
    const sleepTotalMinutes = sleepHours * 60 + sleepMinutes;
    const numCycles = Math.floor(sleepTotalMinutes / 90);
    const cycleStage = getCycleStage(numCycles);

    return `You completed ${numCycles} sleep cycles. You woke up during the ${cycleStage} stage.`;
    }

    function getCycleStage(numCycles) {
    const stages = ['light', 'deep', 'REM'];
    return stages[numCycles % stages.length];
    }

        function calculateSleepCycleInfo(numCycles, sleepHours, sleepMinutes) {
            const stages = ['light', 'deep', 'REM'];
            const cycleStage = stages[numCycles % stages.length];
            
            let cycleInfo = "";

            if (cycleStage === 'light') {
                cycleInfo = "During light sleep, your body is transitioning from wakefulness to deeper sleep stages. Memory consolidation and overall restoration take place.";
            } else if (cycleStage === 'deep') {
                cycleInfo = "Deep sleep is the most restorative stage. Growth hormone is released, promoting tissue repair and growth. Physical recovery, immune system function, and overall well-being occur during this stage.";
            } else if (cycleStage === 'REM') {
                cycleInfo = "During REM sleep, vivid dreaming and cognitive processing take place. This stage is important for emotional regulation, memory consolidation, and creative problem-solving.";
            }

            return cycleInfo;
        }

        trackButton.addEventListener("click", function(event) {
            event.preventDefault(); 

            const sleepTime = document.getElementById("sleep-time").value;
            const wakeTime = document.getElementById("wake-time").value;

            const { hours, minutes } = calculateSleepDuration(sleepTime, wakeTime);
            const numCycles = Math.floor((hours * 60 + minutes) / 90);
            const sleepCycle = calculateSleepCycle(hours, minutes);
            const sleepCycleInfo = calculateSleepCycleInfo(numCycles, hours, minutes);

            sleepDurationText.textContent = `Total Sleep Duration: ${hours} hours and ${minutes} minutes`;
            sleepCycleText.textContent = `Sleep Cycle: ${sleepCycle}`;
            sleepCycleInfoText.textContent = `Sleep Cycle Info: ${sleepCycleInfo}`;

            sleepForm.style.display = "none";
            sleepResults.style.display = "block";
        });

});