export const COLORSCALE = [
    "#023858",
    "#045a8d",
    "#0570b0",
    "#3690c0",
    "#74a9cf",
    "#a6bddb",
    "#a6bddb",
    "#74a9cf",
    "#3690c0",
    "#0570b0",
    "#045a8d",
    "#023858"
]

export const PERCENTAGES = [
    "0%",
    "8.3%",
    "16.7%",
    "25%",
    "33.3%",
    "41.7%",
    "50%",
    "58.3%",
    "66.7%",
    "75%",
    "83.3%",
    "91.7%",
    "100%"
]

export function getArrowDirectionUtil(column, websiteData, statistics) {
    if (websiteData[column] > statistics[column]['50%']){
        return 'up'
    } else if (websiteData[column] < statistics[column]['50%']){
        return 'down'
    } else return 'even';
}

export function calculateArrowColorUtil(column, websiteData, statistics) {
    for (let step = 0; step < 12; step++) {
        if (websiteData[column] >= statistics[column][PERCENTAGES[step]]
            && websiteData[column] < statistics[column][PERCENTAGES[step + 1]]) {
            return COLORSCALE[step];
        }
    }
}