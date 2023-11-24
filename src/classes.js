const fs = require('fs')

let assetsProvider = "https://canary.discord.com/assets/"



function main(){

    let t = {}

    let r = {}


    function a(b){
        return t[b]
    }

    return fetch("https://canary.discord.com/app")
    .then(e=>{return e.text()})
    .then(e=>{
        const scripts = e.match(/<script src="\/assets\/[a-z0-9]+\.js"[^>]+><\/script>/g)
        let links = scripts.map((s) => s.match(/src="[^"]+"/g)?.[0].slice(13, -1))
        fetch(assetsProvider+links[0])
        .then(k=>{
            return k.text()
        }).then(k=>{
            console.log(assetsProvider+links[0])
            eval(k)
            let functions = Object.keys(webpackChunkdiscord_app[0][1])
            let funct = webpackChunkdiscord_app[0][1]
            for (function_ of functions){
                let e = {}
                try{
                    funct[function_](e,null,a)
                    t[function_] = e.exports
                    functions.indexOf(elementToRemove);
                    if (indexToRemove !== -1) {
                        functions.splice(indexToRemove, 1);
                    }
                }catch{}
                
            }
            for (function_ of functions){
                let e = {}
                try{
                    funct[function_](e,null,a)
                    t[function_] = e.exports
                    indexToRemove = functions.indexOf(function_);
                    if (indexToRemove !== -1) {
                        functions.splice(indexToRemove, 1);
                    }
                }catch{}
                
            }
            fetch(assetsProvider+links[1]).then(e=>{
                return e.text()
            }).then(l=>{
                eval(l)
                let functions = Object.keys(webpackChunkdiscord_app[0][1])
                let funct = webpackChunkdiscord_app[0][1]
                for (function_ of functions){
                    let e = {}
                    
                    funct[function_](e,null,a)
                    for (key of Object.keys(e.exports)){
                        r[key] = e.exports[key]
                    }
                    
                    
                }
                console.log(r)
                fs.writeFile('./classes.json',JSON.stringify(r), err => {
                    if (err) {
                        console.log('Error writing file', err)
                    } else {
                        console.log('Successfully wrote file')
                    }
                })
            })
         
        })
       
    })
}
main()
