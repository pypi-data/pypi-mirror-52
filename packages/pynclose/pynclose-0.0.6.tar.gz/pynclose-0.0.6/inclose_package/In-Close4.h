#pragma once
#include "hr_time.h"
#include "crossplatform.h"
#include "targetver.h"
int niam(void);
string run_search(string data_filename, unsigned int minimal_intent, unsigned int minimal_extent);
void InClose   (const int c, const int y, VECTOR_TYPE *Bparent);
void InCloseMin(const int c, const int y, VECTOR_TYPE *Bparent);
void InCloseDendo(const int c, const int y, const VECTOR_TYPE *Bparent);
void sortRows();
void sortColumns();
void sortColumnsR();
void calcAandBsizes();
void cxtFileInput();
void datFileInput();
void outputConcepts();
void outputConceptsNames();
void outputNoConsBySize();
void outputContext();
void cxtFileOutput();
void outputJSONConcepts();
void outputConceptTreeDendrogram();
void outputConceptTree();
void outputConceptsNamesCSV();
