/*
 *  metrics.rs
 *
 *  Language, Variation and Change
 *  Hauptseminar, WS16-17
 *  University of Tuebingen
 *
 *  Christopher Dilley, Inna Pyrina, Erik Schill
 *
 *  Part 1: Reading data, Levenshtein distances, Lexical metrics
 *  Author: Erik Schill
 */

use std::cmp::min;
use std::collections::HashMap;
use std::f64::consts::E;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::io::{BufRead, Write};
use std::mem::swap;

/*
 * Read the ielex-4-26-2016.csv file into a hashmap.
 */
fn read_file(file: File) -> HashMap<String, Vec<(String, String)>> {

  let reader = BufReader::new(file);
  let mut data = HashMap::new();

  for line in reader.lines().skip(1) {
    let line = line.unwrap();
    let mut fields = line.split(",").skip(1).take(3);

    if let Some(lang) = fields.next() {
      let words = data.entry(lang.to_owned()).or_insert(Vec::new());

      if let (Some(word), Some(ipa)) = (fields.next(), fields.next()) {
        words.push((word.to_owned(), ipa.to_owned()));
      }
    }
  }

  data
}

/*
 * Write the lexical metrics to the output file.
 */
fn write_file(
  file: File,
  data: &HashMap<String, Vec<(String, String)>>,
  metrics: &HashMap<String, Vec<Vec<f64>>>
) {

  let mut writer = BufWriter::new(file);

  for (lang, m_vec) in metrics {
    let words = data.get(lang).unwrap();

    writeln!(writer, "# {}", lang).unwrap();
    for (i, vals) in m_vec.iter().enumerate() {
      write!(writer, "{}={}\t", words[i].0, words[i].1).unwrap();

      for val in vals {
        write!(writer, "{} ", val).unwrap();
      }
      writeln!(writer, "").unwrap();
    }
  }
}

/*
 * Computes the levenshtein distance.
 */
fn d(w1: &str, w2: &str) -> usize {

  if w1 == w2 { return 0; }

  let mut v1: Vec<usize> = (0..w2.chars().count() + 1).collect();
  let mut v2: Vec<usize> = vec![0; v1.len()];

  for (i, c1) in w1.chars().enumerate() {
    v2[0] = i + 1;
    for (j, c2) in w2.chars().enumerate() {
      let cost = if c1 == c2 { 0 } else { 1 };
      v2[j+1] = min(v2[j] + 1, min(v1[j] + cost, v1[j+1] + 1));
    }
    swap(&mut v1, &mut v2);
  }

  v1[w2.chars().count()]
}

/*
 * Adjusted levenshtein distance.
 */
fn d2(w1: &str, w2: &str) -> f64 {

  let (len1, len2) = (w1.chars().count(), w2.chars().count());
  2.0 * d(w1, w2) as f64 / (len1 + len2) as f64
}

/*
 * Calculate the edit distances and the norms at the same time.
 */
fn distances_norms(
  data: &HashMap<String, Vec<(String, String)>>,
) -> (HashMap<String, Vec<f64>>, HashMap<String, Vec<f64>>) {

  let mut distances = HashMap::with_capacity(data.len());
  let mut norms = HashMap::with_capacity(data.len());

  for (lang, words) in data {
    let n_distances = words.len() * (words.len() + 1) / 2;

    let mut d_vec = Vec::with_capacity(n_distances);
    let mut n_vec = vec![0.0; words.len()];

    for i in 0..words.len() {
      for j in 0..i+1 {
        let ed2 = E.powf(-d2(&words[i].1, &words[j].1));

        d_vec.push(ed2);

        if i != j {
          n_vec[j] += ed2;
        }
        n_vec[i] += ed2;
      }
    }
    distances.insert(lang.to_owned(), d_vec);
    norms.insert(lang.to_owned(), n_vec);
  }

  (distances, norms)
}

/*
 * Construct the lexical metrics from the data.
 */
fn lexical_metrics(
  distances: &HashMap<String, Vec<f64>>,
  norms: &HashMap<String, Vec<f64>>
) -> HashMap<String, Vec<Vec<f64>>> {

  let mut metrics = HashMap::new();

  for (lang, n_vec) in norms {
    let d_vec = distances.get(lang).unwrap();
    let mut metric = Vec::with_capacity(distances.len());

    for i in 0..n_vec.len() {
      let mut m_vec = Vec::with_capacity(n_vec.len());

      for j in 0..n_vec.len() {
        let norm = n_vec[j];
        let (i, j) = if i < j { (j, i) } else { (i, j) };
        let ed2 = d_vec[i * (i + 1) / 2 + j];
        let conf_prob = (ed2 / norm * (n_vec.len() as f64))
                      / (n_vec.len() * n_vec.len()) as f64;

        m_vec.push(conf_prob);
      }
      metric.push(m_vec);
    }
    metrics.insert(lang.to_owned(), metric);
  }

  metrics
}

/*
 * The main method.
 */
fn main() {

  let infile = File::open("ielex-4-26-2016.csv").unwrap();
  let data = read_file(infile);
  println!("File read.");
  let (distances, norms) = distances_norms(&data);
  println!("Distances and norms computed.");
  let metrics = lexical_metrics(&distances, &norms);
  println!("Lexical metrics constructed.");
  let outfile = File::create("lm_output").unwrap();
  write_file(outfile, &data, &metrics);
  println!("File written: lm_output");
}

