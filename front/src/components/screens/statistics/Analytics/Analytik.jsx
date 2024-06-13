import React from "react";
import ReportDiv from '../ReportDiv'
// import <CChart> from '@cu'
import ScrollingCharts from '../scrollDiagrams'
import DiagramPercent from './DiagramPercent'
import LinearChart from './LinearDiagramm.tsx'
import BarsDiagram from './BarDiagram.tsx'
import PieChartWithLabel from './PieChartWithLabel.tsx'

const ThirdTab = () => {

  const data = [{label: "Менеджер", values:
    ["50", "40", "10"]},
    {label: "Педагог", values:
    ["50", "40", "10"]
},
{label: "Руководитель", values:
    ["50", "40", "10"]
}]

const pieChartData =  [ { value: 30, label: "Хорошо", color: "rgba(223, 237, 231, 1)" },
{ value: 30, label: "Нормальный уровень", color: "rgba(246, 245, 232, 1)" },
{ value: 30, label: "Низкий уровень", color: "rgba(240, 229, 227, 1)" },

]

  return (
    <div className="FirstTab">
      <div className="report__section" style={{"height": "140px", "margin-bottom": "40px"}}>
      <ReportDiv label="Средний балл выгорания" width="146px" height="139px"><DiagramPercent/></ReportDiv>
      <ReportDiv label="Аналитика по филиалам" width="442px" height="139px"><ScrollingCharts data={data}/></ReportDiv>
      <ReportDiv label="Аналитика по должностной категории" width="442px" height="139px"><ScrollingCharts data={data}/></ReportDiv>
      </div>

      <div className="report__section" style={{"height": "279px"}}>
      <ReportDiv label="Сравнительный анализ" width="628px" height="279px"><BarsDiagram width={628} height={279}/></ReportDiv>
      <ReportDiv label="Аналитика по стажу работы" width="201px" height="279px"><PieChartWithLabel data={pieChartData} label={54} width={201} height={279}/></ReportDiv>
      <ReportDiv label="Аналитика по фазам" width="201px" height="279px"><>
      <div className="inner__repoprt__div">
        <p>Истощение</p><p style={{"margin-left": "auto"}}>54</p>
        <p>Деперсонализация</p><p style={{"margin-left": "auto"}}>12</p>
        <p>Редукция</p><p style={{"margin-left": "auto"}}></p>
      </div>

        </></ReportDiv>
    </div>
    </div>

  );
};

export default ThirdTab;