/*
 * axis_controller_data.c
 *
 * Code generation for model "axis_controller".
 *
 * Model version              : 1.6
 * Simulink Coder version : 8.6 (R2014a) 27-Dec-2013
 * C source code generated on : Thu Mar 02 20:02:09 2023
 *
 * Target selection: grt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */
#include "axis_controller.h"
#include "axis_controller_private.h"

/* Block parameters (auto storage) */
P_axis_controller_T axis_controller_P = {
  250.0,                               /* Variable: v_max
                                        * Referenced by: '<Root>/i'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<Root>/i'
                                        */
  -2.0,                                /* Computed Parameter: p3_A
                                        * Referenced by: '<Root>/p3'
                                        */
  -2.0,                                /* Computed Parameter: p3_C
                                        * Referenced by: '<Root>/p3'
                                        */
  2.0,                                 /* Computed Parameter: p3_D
                                        * Referenced by: '<Root>/p3'
                                        */
  -2.0,                                /* Computed Parameter: p2_A
                                        * Referenced by: '<Root>/p2'
                                        */
  -2.0,                                /* Computed Parameter: p2_C
                                        * Referenced by: '<Root>/p2'
                                        */
  2.0,                                 /* Computed Parameter: p2_D
                                        * Referenced by: '<Root>/p2'
                                        */
  -0.33333333333333331,                /* Computed Parameter: p1_A
                                        * Referenced by: '<Root>/p1'
                                        */
  0.22222222222222221,                 /* Computed Parameter: p1_C
                                        * Referenced by: '<Root>/p1'
                                        */
  0.33333333333333331,                 /* Computed Parameter: p1_D
                                        * Referenced by: '<Root>/p1'
                                        */
  -3.0,                                /* Computed Parameter: c_A
                                        * Referenced by: '<Root>/c'
                                        */
  -8.0,                                /* Computed Parameter: c_C
                                        * Referenced by: '<Root>/c'
                                        */
  3.0,                                 /* Computed Parameter: c_D
                                        * Referenced by: '<Root>/c'
                                        */
  1.0                                  /* Expression: 1
                                        * Referenced by: '<Root>/k_V7'
                                        */
};
