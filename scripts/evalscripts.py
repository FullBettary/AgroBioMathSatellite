evalscript_ndvi = '''
    //VERSION=3
  function setup() {
      return {
          input: ["B03","B04", "B08", "dataMask"],
          output: [
              { id: "default", bands: 4 },
        { id: "index", bands: 1, sampleType: "FLOAT32" },
              { id: "eobrowserStats", bands: 2, sampleType: 'FLOAT32' },
              { id: "dataMask", bands: 1 }
          ]
        };
  }

  function evaluatePixel(samples) {
      let val = index(samples.B08, samples.B04);
      let imgVals = null;
      // The library for tiffs works well only if there is only one channel returned.
      // So we encode the "no data" as NaN here and ignore NaNs on frontend.
      const indexVal = samples.dataMask === 1 ? val : NaN;

      if (val<-0.5) imgVals = [0.05,0.05,0.05,samples.dataMask];
      else if (val<-0.2) imgVals = [0.75,0.75,0.75,samples.dataMask];
      else if (val<-0.1) imgVals = [0.86,0.86,0.86,samples.dataMask];
      else if (val<0) imgVals = [0.92,0.92,0.92,samples.dataMask];
      else if (val<0.025) imgVals = [1,0.98,0.8,samples.dataMask];
      else if (val<0.05) imgVals = [0.93,0.91,0.71,samples.dataMask];
      else if (val<0.075) imgVals = [0.87,0.85,0.61,samples.dataMask];
      else if (val<0.1) imgVals = [0.8,0.78,0.51,samples.dataMask];
      else if (val<0.125) imgVals = [0.74,0.72,0.42,samples.dataMask];
      else if (val<0.15) imgVals = [0.69,0.76,0.38,samples.dataMask];
      else if (val<0.175) imgVals = [0.64,0.8,0.35,samples.dataMask];
      else if (val<0.2) imgVals = [0.57,0.75,0.32,samples.dataMask];
      else if (val<0.25) imgVals = [0.5,0.7,0.28,samples.dataMask];
      else if (val<0.3) imgVals = [0.44,0.64,0.25,samples.dataMask];
      else if (val<0.35) imgVals = [0.38,0.59,0.21,samples.dataMask];
      else if (val<0.4) imgVals = [0.31,0.54,0.18,samples.dataMask];
      else if (val<0.45) imgVals = [0.25,0.49,0.14,samples.dataMask];
      else if (val<0.5) imgVals = [0.19,0.43,0.11,samples.dataMask];
      else if (val<0.55) imgVals = [0.13,0.38,0.07,samples.dataMask];
      else if (val<0.6) imgVals = [0.06,0.33,0.04,samples.dataMask];
      else imgVals = [0,0.27,0,samples.dataMask];    

      return {
        default: imgVals,
        index: [indexVal],
        eobrowserStats:[val,isCloud(samples)?1:0],
        dataMask: [samples.dataMask]
      };
  }

  function isCloud(samples){
      const NGDR = index(samples.B03, samples.B04);
      const bRatio = (samples.B03 - 0.175) / (0.39 - 0.175);
      return bRatio > 1 || (bRatio > 0 && NGDR > 0);
  }
'''
evalscript_nature_color = '''
  //VERSION=3
  let minVal = 0.0;
  let maxVal = 0.4;

  let viz = new HighlightCompressVisualizer(minVal, maxVal);

  function setup() {
    return {
      input: ["B04", "B03", "B02","dataMask"],
      output: { bands: 4 }
    };
  }

  function evaluatePixel(samples) {
      let val = [samples.B04, samples.B03, samples.B02,samples.dataMask];
      return viz.processList(val);
  }
'''

evalscript_get_all_bands = ''' 

  //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12"],
                units: "DN"
            }],
            output: {
                bands: 13,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B01,
                sample.B02,
                sample.B03,
                sample.B04,
                sample.B05,
                sample.B06,
                sample.B07,
                sample.B08,
                sample.B8A,
                sample.B09,
                sample.B10,
                sample.B11,
                sample.B12];
    }

'''