(function () {
    // 'use strict';

    angular
        .module('filters.filters')
        .filter('capFirst', function (){
            return function (sentence){
                    console.log(sentence);
                    var word_arr = sentence.split(" ");
                    console.log(word_arr);
                    var new_sentence = '';
                    console.log(new_sentence);
                    for(i in word_arr){
                        console.log(i);
                        new_sentence += word_arr[i].substring(0,1).toUpperCase()+word_arr[i].slice(1) + " ";
                    }
                    console.log(new_sentence);
                    return new_sentence;
                }
        })
        .filter('parseDate', function (){
            return function (date){
                    console.log(date);
                    var s = date;
                    var a = s.split(/[^0-9]/);
                    return new Date (a[0],a[1]-1,a[2],a[3],a[4],a[5] );
                }
        })
        // .filter('escapeUrl', function (){
        //     return function (url){
        //             console.log(url);
        //             console.log(window.encodeURIComponent(url));
        //             return window.encodeURIComponent(url);
        //         }
        // })


}());
