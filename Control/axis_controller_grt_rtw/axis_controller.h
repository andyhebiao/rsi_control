/*
 * axis_controller.h
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
#ifndef RTW_HEADER_axis_controller_h_
#define RTW_HEADER_axis_controller_h_
#include <float.h>
#include <string.h>
#include <stddef.h>
#ifndef axis_controller_COMMON_INCLUDES_
# define axis_controller_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"
#include "rt_logging.h"
#endif                                 /* axis_controller_COMMON_INCLUDES_ */

#include "axis_controller_types.h"

/* Shared type includes */
#include "multiword_types.h"
#include "rt_nonfinite.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetBlkStateChangeFlag
# define rtmGetBlkStateChangeFlag(rtm) ((rtm)->ModelData.blkStateChange)
#endif

#ifndef rtmSetBlkStateChangeFlag
# define rtmSetBlkStateChangeFlag(rtm, val) ((rtm)->ModelData.blkStateChange = (val))
#endif

#ifndef rtmGetContStateDisabled
# define rtmGetContStateDisabled(rtm)  ((rtm)->ModelData.contStateDisabled)
#endif

#ifndef rtmSetContStateDisabled
# define rtmSetContStateDisabled(rtm, val) ((rtm)->ModelData.contStateDisabled = (val))
#endif

#ifndef rtmGetContStates
# define rtmGetContStates(rtm)         ((rtm)->ModelData.contStates)
#endif

#ifndef rtmSetContStates
# define rtmSetContStates(rtm, val)    ((rtm)->ModelData.contStates = (val))
#endif

#ifndef rtmGetDerivCacheNeedsReset
# define rtmGetDerivCacheNeedsReset(rtm) ((rtm)->ModelData.derivCacheNeedsReset)
#endif

#ifndef rtmSetDerivCacheNeedsReset
# define rtmSetDerivCacheNeedsReset(rtm, val) ((rtm)->ModelData.derivCacheNeedsReset = (val))
#endif

#ifndef rtmGetFinalTime
# define rtmGetFinalTime(rtm)          ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetIntgData
# define rtmGetIntgData(rtm)           ((rtm)->ModelData.intgData)
#endif

#ifndef rtmSetIntgData
# define rtmSetIntgData(rtm, val)      ((rtm)->ModelData.intgData = (val))
#endif

#ifndef rtmGetOdeF
# define rtmGetOdeF(rtm)               ((rtm)->ModelData.odeF)
#endif

#ifndef rtmSetOdeF
# define rtmSetOdeF(rtm, val)          ((rtm)->ModelData.odeF = (val))
#endif

#ifndef rtmGetOdeY
# define rtmGetOdeY(rtm)               ((rtm)->ModelData.odeY)
#endif

#ifndef rtmSetOdeY
# define rtmSetOdeY(rtm, val)          ((rtm)->ModelData.odeY = (val))
#endif

#ifndef rtmGetRTWLogInfo
# define rtmGetRTWLogInfo(rtm)         ((rtm)->rtwLogInfo)
#endif

#ifndef rtmGetZCCacheNeedsReset
# define rtmGetZCCacheNeedsReset(rtm)  ((rtm)->ModelData.zCCacheNeedsReset)
#endif

#ifndef rtmSetZCCacheNeedsReset
# define rtmSetZCCacheNeedsReset(rtm, val) ((rtm)->ModelData.zCCacheNeedsReset = (val))
#endif

#ifndef rtmGetdX
# define rtmGetdX(rtm)                 ((rtm)->ModelData.derivs)
#endif

#ifndef rtmSetdX
# define rtmSetdX(rtm, val)            ((rtm)->ModelData.derivs = (val))
#endif

#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

#ifndef rtmGetStopRequested
# define rtmGetStopRequested(rtm)      ((rtm)->Timing.stopRequestedFlag)
#endif

#ifndef rtmSetStopRequested
# define rtmSetStopRequested(rtm, val) ((rtm)->Timing.stopRequestedFlag = (val))
#endif

#ifndef rtmGetStopRequestedPtr
# define rtmGetStopRequestedPtr(rtm)   (&((rtm)->Timing.stopRequestedFlag))
#endif

#ifndef rtmGetT
# define rtmGetT(rtm)                  (rtmGetTPtr((rtm))[0])
#endif

#ifndef rtmGetTFinal
# define rtmGetTFinal(rtm)             ((rtm)->Timing.tFinal)
#endif

/* Block signals (auto storage) */
typedef struct {
  real_T p3;                           /* '<Root>/p3' */
  real_T p2;                           /* '<Root>/p2' */
  real_T Sum7;                         /* '<Root>/Sum7' */
  real_T k_V7;                         /* '<Root>/k_V7' */
} B_axis_controller_T;

/* Continuous states (auto storage) */
typedef struct {
  real_T i_CSTATE;                     /* '<Root>/i' */
  real_T p3_CSTATE;                    /* '<Root>/p3' */
  real_T p2_CSTATE;                    /* '<Root>/p2' */
  real_T p1_CSTATE;                    /* '<Root>/p1' */
  real_T c_CSTATE;                     /* '<Root>/c' */
} X_axis_controller_T;

/* State derivatives (auto storage) */
typedef struct {
  real_T i_CSTATE;                     /* '<Root>/i' */
  real_T p3_CSTATE;                    /* '<Root>/p3' */
  real_T p2_CSTATE;                    /* '<Root>/p2' */
  real_T p1_CSTATE;                    /* '<Root>/p1' */
  real_T c_CSTATE;                     /* '<Root>/c' */
} XDot_axis_controller_T;

/* State disabled  */
typedef struct {
  boolean_T i_CSTATE;                  /* '<Root>/i' */
  boolean_T p3_CSTATE;                 /* '<Root>/p3' */
  boolean_T p2_CSTATE;                 /* '<Root>/p2' */
  boolean_T p1_CSTATE;                 /* '<Root>/p1' */
  boolean_T c_CSTATE;                  /* '<Root>/c' */
} XDis_axis_controller_T;

#ifndef ODE3_INTG
#define ODE3_INTG

/* ODE3 Integration Data */
typedef struct {
  real_T *y;                           /* output */
  real_T *f[3];                        /* derivatives */
} ODE3_IntgData;

#endif

/* External inputs (root inport signals with auto storage) */
typedef struct {
  real_T reference;                    /* '<Root>/reference' */
  real_T pre_pose;                     /* '<Root>/pre_pose' */
} ExtU_axis_controller_T;

/* External outputs (root outports fed by signals with auto storage) */
typedef struct {
  real_T velocity;                     /* '<Root>/velocity' */
} ExtY_axis_controller_T;

/* Parameters (auto storage) */
struct P_axis_controller_T_ {
  real_T v_max;                        /* Variable: v_max
                                        * Referenced by: '<Root>/i'
                                        */
  real_T i_IC;                         /* Expression: 0
                                        * Referenced by: '<Root>/i'
                                        */
  real_T p3_A;                         /* Computed Parameter: p3_A
                                        * Referenced by: '<Root>/p3'
                                        */
  real_T p3_C;                         /* Computed Parameter: p3_C
                                        * Referenced by: '<Root>/p3'
                                        */
  real_T p3_D;                         /* Computed Parameter: p3_D
                                        * Referenced by: '<Root>/p3'
                                        */
  real_T p2_A;                         /* Computed Parameter: p2_A
                                        * Referenced by: '<Root>/p2'
                                        */
  real_T p2_C;                         /* Computed Parameter: p2_C
                                        * Referenced by: '<Root>/p2'
                                        */
  real_T p2_D;                         /* Computed Parameter: p2_D
                                        * Referenced by: '<Root>/p2'
                                        */
  real_T p1_A;                         /* Computed Parameter: p1_A
                                        * Referenced by: '<Root>/p1'
                                        */
  real_T p1_C;                         /* Computed Parameter: p1_C
                                        * Referenced by: '<Root>/p1'
                                        */
  real_T p1_D;                         /* Computed Parameter: p1_D
                                        * Referenced by: '<Root>/p1'
                                        */
  real_T c_A;                          /* Computed Parameter: c_A
                                        * Referenced by: '<Root>/c'
                                        */
  real_T c_C;                          /* Computed Parameter: c_C
                                        * Referenced by: '<Root>/c'
                                        */
  real_T c_D;                          /* Computed Parameter: c_D
                                        * Referenced by: '<Root>/c'
                                        */
  real_T k_V7_Gain;                    /* Expression: 1
                                        * Referenced by: '<Root>/k_V7'
                                        */
};

/* Real-time Model Data Structure */
struct tag_RTM_axis_controller_T {
  const char_T *errorStatus;
  RTWLogInfo *rtwLogInfo;
  RTWSolverInfo solverInfo;

  /*
   * ModelData:
   * The following substructure contains information regarding
   * the data used in the model.
   */
  struct {
    X_axis_controller_T *contStates;
    real_T *derivs;
    boolean_T *contStateDisabled;
    boolean_T zCCacheNeedsReset;
    boolean_T derivCacheNeedsReset;
    boolean_T blkStateChange;
    real_T odeY[5];
    real_T odeF[3][5];
    ODE3_IntgData intgData;
  } ModelData;

  /*
   * Sizes:
   * The following substructure contains sizes information
   * for many of the model attributes such as inputs, outputs,
   * dwork, sample times, etc.
   */
  struct {
    int_T numContStates;
    int_T numSampTimes;
  } Sizes;

  /*
   * Timing:
   * The following substructure contains information regarding
   * the timing information for the model.
   */
  struct {
    uint32_T clockTick0;
    uint32_T clockTickH0;
    time_T stepSize0;
    uint32_T clockTick1;
    uint32_T clockTickH1;
    time_T tFinal;
    SimTimeStep simTimeStep;
    boolean_T stopRequestedFlag;
    time_T *t;
    time_T tArray[2];
  } Timing;
};

/* Block parameters (auto storage) */
extern P_axis_controller_T axis_controller_P;

/* Block signals (auto storage) */
extern B_axis_controller_T axis_controller_B;

/* Continuous states (auto storage) */
extern X_axis_controller_T axis_controller_X;

/* External inputs (root inport signals with auto storage) */
extern ExtU_axis_controller_T axis_controller_U;

/* External outputs (root outports fed by signals with auto storage) */
extern ExtY_axis_controller_T axis_controller_Y;

/* Model entry point functions */
extern void axis_controller_initialize(void);
extern void axis_controller_step(void);
extern void axis_controller_terminate(void);

/* Real-time Model object */
extern RT_MODEL_axis_controller_T *const axis_controller_M;

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'axis_controller'
 */
#endif                                 /* RTW_HEADER_axis_controller_h_ */
