function processResult(result){
  $('#hard_predict').html(`Your best chance for compensation is ${result.max_prob} if you file ${result.best_day} days after the incident`);
  makePlot('#vis', result.probs);

}

function makePlot(selector, list_of_probs){
    const yourVlSpec = {
      "$schema": "https://vega.github.io/schema/vega-lite/v3.0.json",
      "description": "A simple bar chart with embedded data.",
      "data": {
        "values": list_of_probs.map((prob, index) => {return {'days': index + 1, 'probability': prob}; })
      },
      "mark": "line",
      "encoding": {
        "x": {"field": "days", "type": "ordinal"},
        "y": {"field": "probability", "type": "quantitative"}
      }
    };

    vegaEmbed(selector, yourVlSpec);
}