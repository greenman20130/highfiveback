import React from 'react'

type Data = {
    percent: number,

};

function DiagramPercent(props: Data){

    return(<>
    <h2 style={{"color": "red", "fontSize": "30px"}}>{props.percent+ "%"}
    </h2>
    {(props.percent > 90) && <p>Bad</p>}
    {(props.percent <= 90 && props.percent > 70) && <p>Bad</p>}
    {(props.percent <= 70 && props.percent > 50) && <p>Bad</p>}
    {(props.percent <= 50 && props.percent > 20) && <p>Normal</p>}
    {(props.percent <= 20) && <p>Normal</p>}

    </>
)
}

export default DiagramPercent;





















