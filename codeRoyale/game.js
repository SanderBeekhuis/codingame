function dist(a, b){
    return Math.sqrt((a.x - b.x) * (a.x - b.x ) + (a.y - b.y)*(a.y - b.y))
}

const gameHeight = 1000
const gameWidth = 1920
const structures = {'None': -1, 'Barracks':2}
const owner = {'None':-1, 'Me': 0, 'Enemy':1}
const creep = {'Knight': 0, 'Archer':1}


class Site{
    constructor(siteId, x, y, radius){
        this.siteId = parseInt(siteId)
        this.x = parseInt(x)
        this.y = parseInt(y)
        this.radius = parseInt(radius)
        this.structureType = structures.None
        this.owner = owner.None
        this.timeToTrain = 0
        this.creepType = null
    }

    update(structureType, owner, timeToTrain, creepType){
        this.structureType = parseInt(structureType)
        this.owner = parseInt(owner)
        this.timeToTrain = parseInt(timeToTrain)
        this.creepType = parseInt(creepType)
    }

    toString(){
        return (`siteId:` + this.siteId+`  x:`+this.x+` y:`+this.y + ` owner ${this.owner}`);
    }
}

class Sites {
    constructor(){
        this.sites = {}
    }

    push(siteId, x, y, radius){
        this.sites[siteId] = (new Site(siteId, x, y, radius));
    }

    toString(){
        return this.sites.toString()
    }

    closestSite(x, y){
        let loc = {x, y}
        let minDist = 100000000000;
        let result = null
        for(let siteId in this.sites){
            let site = this.sites[siteId]
            if (dist(loc, site) < minDist){
                minDist = dist(loc, site)
                result = site
            }
        }
        return result
    }

    centralSite(){
        return this.closestSite(gameWidth/2, gameHeight/2)        
    }

    trainSites(){
        let results = []
        for(let siteId in this.sites){
            let site = this.sites[siteId]
            printErr(site)
            if (site.owner === owner.Me && site.timeToTrain === 0){
                results.push(site)
            }
        }
        return results
    }
}

let sites = new Sites()

var numSites = parseInt(readline());
for (var i = 0; i < numSites; i++) {
    let inputs = readline().split(' ');
    let [siteId, x ,y , radius] = inputs;
    sites.push(siteId, x, y, radius)
}


// game loop
while (true) {
    var inputs = readline().split(' ');
    var gold = parseInt(inputs[0]);
    var touchedSite = parseInt(inputs[1]); // -1 if none
    for (var i = 0; i < numSites; i++) {
        var inputs = readline().split(' ');
        let [siteId, ignore1, ignore2, structureType, owner, timeToTrain, creepType] = inputs
        sites.sites[siteId].update(structureType, owner, timeToTrain, creepType)
    }
    var numUnits = parseInt(readline());
    for (var i = 0; i < numUnits; i++) {
        var inputs = readline().split(' ');
        // var x = parseInt(inputs[0]);
        // var y = parseInt(inputs[1]);
        // var owner = parseInt(inputs[2]);
        // var unitType = parseInt(inputs[3]); // -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        // var health = parseInt(inputs[4]);
    }

    // Write an action using print()
    // To debug: printErr('Debug messages...');


    // First line: A valid queen action
    // Second line: A set of training instructions
    let buildSite = sites.centralSite()
    let trainSites = sites.trainSites()
    print(`BUILD ${buildSite.siteId} BARRACKS-KNIGHT`);
    printErr(trainSites.length)
    if (trainSites.length > 0){
            print(`TRAIN `+trainSites[0].siteId);
    } else {
            print(`TRAIN`);

    }
    
    //TODO if building was succefull move awy from units
}
