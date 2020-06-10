var data_

$(document).ready(function(){
    var _data;
    var _labels;
    fetch(`${window.origin}/data`)
        .then(function(data) {
            return data.json()
        })
        .then(function(dataJSON) {
            
            data_ = dataJSON
            console.log(data_[0].followerData[0])
            console.log(data_[0].followersLabels)

            //CHART 
            //Followers LIKES VS TIME
            let myChart = document.getElementById('myChart').getContext('2d');
            let xChart = new Chart(myChart, {
                type: 'line',
                data: {
                    labels: data_[0].followersLabels,
                    datasets: [{
                        label: "Followers",
                        data: data_[0].followerData,
                        borderWidth: 2,
                        backgroundColor: "#40b680",
                        borderColor: "#6a11cb"
                    }]
                },
                options: {
                    legend:{
                        labels:{
                            fontColor:"white"
                        }
                    },
                    scales: {
                        yAxes: [{
                            gridLines:{
                                display: true,
                                color: "black"
                            },
                            ticks: {
                                beginAtZero: false,
                                fontColor:"white"
                            }
                        }],
                        xAxes: [{
                            gridLines:{
                                display: false,
                            },
                            ticks: {
                                beginAtZero: true,
                                fontColor:"white"
                            }
                        }]
                    }
                }
            });

            //CHART 
            //LIKES VS TIME
            if (data_[1].likesData == null){
                console.log("no likes")
            }
            else{
                let myChart1 = document.getElementById('myChart1').getContext('2d');
                let xChart1 = new Chart(myChart1, {
                    type: 'line',
                    data: {
                        labels: data_[1].likesLabels,
                        datasets: [{
                            label: 'Total Account Likes',
                            data: data_[1].likesData,
                            backgroundColor: "#f5f2d0",
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        legend:{
                            labels:{
                                fontColor:"white"
                            }
                        },
                        scales: {
                            yAxes: [{
                                gridLines:{
                                    display: true,
                                    color: "black"
                                },
                                ticks: {
                                    beginAtZero: false,
                                    fontColor:"white"
                                }
                            }],
                            xAxes: [{
                                gridLines:{
                                    display: false,
                                },
                                ticks: {
                                    beginAtZero: true,
                                    fontColor:"white"
                                }
                            }]
                        }
                    }
                });
            }

            //CHART 
            //AVG LIKES VS TIME
            if(data_[2].avgLikesData == null){
                console.log('no average likes')
            }
            else{
                let myChart2 = document.getElementById('myChart2').getContext('2d');
                let xChart2 = new Chart(myChart2, {
                    type: 'line',
                    data: {
                        labels: data_[2].avgLikesLabels,
                        datasets: [{
                            label: "Followers",
                            data: data_[2].avgLikesData,
                            borderColor: "white",
                            backgroundColor: '#7a2048',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        legend:{
                            labels:{
                                fontColor:"white"
                            }
                        },
                        scales: {
                            yAxes: [{
                                gridLines:{
                                    display: true,
                                    color: "black"
                                },
                                ticks: {
                                    beginAtZero: false,
                                    fontColor:"white"
                                }
                            }],
                            xAxes: [{
                                gridLines:{
                                    display: false,
                                },
                                ticks: {
                                    beginAtZero: true,
                                    fontColor:"white"
                                }
                            }]
                        }
                    }
                });
            }


        })
    
});




