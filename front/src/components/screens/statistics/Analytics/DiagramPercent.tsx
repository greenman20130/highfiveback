import React from 'react'
import './Percent.svg'

type Data = {
    percent: number,

};

function DiagramPercent(props: Data){

    return(<div style={{"backgroundImage": "url('./Percent.svg'"}}>
    <h2 style={{"color": "red", "fontSize": "30px", "marginLeft": "50px", "marginTop": "50px"}}>{props.percent+ "%"}
    </h2>
    {(props.percent > 90) && <p>Bad</p>}
    {(props.percent <= 90 && props.percent > 70) && <p></p>}
    {(props.percent <= 70 && props.percent > 50) && <p></p>}
    {(props.percent <= 50 && props.percent > 20) && <p></p>}
    {(props.percent <= 20) && <p>Normal</p>}

    </div>
)
}

export default DiagramPercent;





















