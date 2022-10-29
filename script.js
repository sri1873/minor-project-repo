var path1 = ''
var path2 = ''
var loadFile = (event, id) => {
    var output = document.getElementById(id);
    console.log((event.target.files[0]))
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = () => {
        URL.revokeObjectURL(output.src) // free memory
    }
};
const onsub = (event, id1, id2) => {
    event.preventDefault()
    var output=''
    console.log(path1, path2)
    axios(`http://127.0.0.1:8000/login?path1=${path1}&path2=${path2}`, {
        method: "GET",mode:'no-cors', headers: {
            'Access-Control-Allow-Origin': '*',
        }
    }).then(res => { document.getElementById('result').innerHTML = res.data})
    

}
const setpath1 = (e) => {
    path1 = e.target.value
}
const setpath2 = (e) => {
    path2 = e.target.value
}