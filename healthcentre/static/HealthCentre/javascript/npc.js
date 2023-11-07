// create constants for the form and form controls
const newPeriodFormElement = document.getElementsByTagName("form")[0];
const startDateInputElement = document.getElementById("start-date");
const endDateInputElement = document.getElementById("end-date");
const pastPeriodContainer = document.getElementById("past-periods");

// storage key - app-wide constant
const storage_key = "period-tracker";

//adding event listener to form submission to save the entered data into local storage
newPeriodFormElement.addEventListener('submit', (event)=>{
    
    //preventing the form from submitting to the server (client-side only)
    event.preventDefault();

    //get the start and end dates from the user input to the form
    //value stored in the start date input is stored in startDate const
    const startDate = startDateInputElement.value;
    const endDate = endDateInputElement.value;

    //check for the validity of the dates
    if(checkInvalidity(startDate, endDate)){
        //if dates are invalid then exit
        return;
    }

    //otherwise store the new period in our client-end storage
    storeNewPeriodDates(startDate , endDate);

    //fetch the past dates after storing for date entry
    fetchPastPeriodDates();

    //Resetting the form for date entry again
    newPeriodFormElement.reset();
});


//user-defined function to check the validity of entered dates
const checkInvalidity=(startDate , endDate) => {
    if(startDate > endDate || !startDate || !endDate) {
        //since the dates are invalid clear the form data
        newPeriodFormElement.reset();
        //return true for invalidity
        return true;
    }
    //return false for invalidity
    return false;
}


//user-defined function to store the period dates
storeNewPeriodDates=(startDate , endDate)=> {
    //retrieving data from storage
    const periodsData = getAllStoredPeriodDates();

    //adding new dates to the end of the array objects
    periodsData.push({startDate , endDate});

    //sort for proper ordering
    periodsData.sort((a, b) => {
        return new Date(b.startDate) - new Date(a.startDate);
    });

    // store the updated array back into the storage
    window.localStorage.setItem(storage_key, JSON.stringify(periodsData));
}

//user-defined function to retrieve all the stored data
getAllStoredPeriodDates = () => {
    const data = window.localStorage.getItem(storage_key);

    //if no period dates were stored default to empty array
    const periodsData = data ? JSON.parse(data) : [];
    console.dir(periodsData);
    console.log(periodsData);
    return periodsData;
}

//user-defined function fetch past period dates
fetchPastPeriodDates = () => {
    const pastPeriodHeader = document.createElement("h2");
    const pastPeriodList = document.createElement("ul");
    const periodsData = getAllStoredPeriodDates();

    //no data
    if(periodsData.length === 0){
        return;
    }

    //clear previous list to replace with updated list
    pastPeriodContainer.innerHTML="";
    pastPeriodHeader.textContent = "Past periods";

    //looping over all period dates and fetching them
    periodsData.forEach((element) => {
        const periodElement = document.createElement("li");
        periodElement.textContent = `From ${formatDate(
            element.startDate ,
        )} to ${formatDate(element.endDate)}`;
        pastPeriodList.appendChild(periodElement);
    });

    pastPeriodContainer.appendChild(pastPeriodHeader);
    pastPeriodContainer.appendChild(pastPeriodList);
}

//user-defined function to format the date
formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {timeZone:"IST"});
}

fetchPastPeriodDates();
console.clear();
