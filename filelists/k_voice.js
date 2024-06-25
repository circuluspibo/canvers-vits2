const fs = require('fs')
const exec = require('child_process').exec

const list = []

const dirs = fs.readdirSync('./TTS')

for (const dir of dirs){
    if(dir.startsWith('k_')){
        list.push(dir)
    }
}

fs.writeFileSync('k_voice.txt',list.join('\n'))
