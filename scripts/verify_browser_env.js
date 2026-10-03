// Simulate browser global window
global.window = global;

require('../data/geospatial_national.js');
require('../data/multivariate_jateng.js');
require('../data/hierarchy_jateng.js');

console.log("GEOSPATIAL_DATA loaded, features:", window.GEOSPATIAL_DATA.features.length);
console.log("MULTIVARIATE_DATA loaded, unit_count:", window.MULTIVARIATE_DATA.metadata.unit_count);
console.log("HIERARCHY_DATA loaded, root:", window.HIERARCHY_DATA.name);

// Check features
const feats = window.GEOSPATIAL_DATA.features;
let withTPT = 0;
let withPop = 0;
let withWork = 0;
for (const f of feats) {
    if (f.properties.tpt !== null && f.properties.tpt !== undefined) withTPT++;
    if (f.properties.total_penduduk > 0) withPop++;
    if (f.properties.total_bekerja > 0) withWork++;
}

console.log(`Summary of 515 Kab/Kota:\n- With TPT: ${withTPT}/515\n- With Population: ${withPop}/515\n- With Workers: ${withWork}/515`);
