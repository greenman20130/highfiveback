import React from "react";
import ReportDiv from '../4/ReportDiv.tsx'
// import ScrollingCharts from './scrollDiagrams'
// import DiagramPercent from './DiagramPercent'
import LinearChart from './LinearDiagramm.tsx'
import './Dynamic.css'
import PieChartWithLabel from "./PieChartWithLabel.tsx";

const pieChartData =  [ { value: 30, label: "Хорошо", color: "rgba(223, 237, 231, 1)" },
{ value: 30, label: "Нормальный уровень", color: "rgba(246, 245, 232, 1)" },
{ value: 30, label: "Низкий уровень", color: "rgba(240, 229, 227, 1)" },

]
const pieChartData2 =  [ { value: 30, label: "Хорошо", color: "rgba(223, 237, 231, 1)" },
{ value: 30, label: "Нормальный уровень", color: "rgba(246, 245, 232, 1)" },
{ value: 30, label: "Низкий уровень", color: "rgba(240, 229, 227, 1)" },

]


const calcResult =  "С момента внедрения  мер по снижению уровня выгорания в компании наблюдается устойчивая тенденция к улучшению."
const calcResultCont =  "средний балл снизился до 20 и свидетельствует о хорошем прогрессе."
const time = "В настоящее время: "
const calcRes2 = "Борьба с выгоранием — это непрерывный процесс, требующий постоянного внимания и усилий. "
const calcRes2Cont = "Создание здоровой рабочей среды — это инвестиция, которая окупится повышением производительности труда и снижением текучести кадров."


const  ForthTab = () => {
  return (
    <div className="SecondTab">
       <div className="report__section" style={{"height": "186px", "margin-bottom": "40px"}}>
      <ReportDiv label="Сравнительный анализ среднего показателя" width="884px" height="186px"><LinearChart height={186} width={884}/></ReportDiv>
      <ReportDiv label="Динамика" width="186px" height="186px">
        <>
        <p>{calcResult}</p>
        <p><span style={{"font-size": "9px", "font-weight": "700"}}>{time}</span>{calcResultCont}</p>
        </>
      </ReportDiv>
      </div>

      <div className="report__section" style={{"height": "295px", "margin-bottom": "40px"}}>
      <ReportDiv label="До" width="422px" height="295px"><PieChartWithLabel data={pieChartData} label={54} width={201} height={279}/></ReportDiv>
      <ReportDiv label="После" width="422px" height="295px"><PieChartWithLabel data={pieChartData2} label={54} width={201} height={279}/></ReportDiv>
      <ReportDiv label="Помните" width="186px" height="295px">
        <>
        <p>{calcRes2}</p>
        <p>{calcRes2Cont}</p>
        </>
        </ReportDiv>

      </div>

    </div>
  );
};
export default ForthTab;