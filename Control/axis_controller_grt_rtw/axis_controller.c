/*
 * axis_controller.c
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

/* Block signals (auto storage) */
B_axis_controller_T axis_controller_B;

/* Continuous states */
X_axis_controller_T axis_controller_X;

/* External inputs (root inport signals with auto storage) */
ExtU_axis_controller_T axis_controller_U;

/* External outputs (root outports fed by signals with auto storage) */
ExtY_axis_controller_T axis_controller_Y;

/* Real-time model */
RT_MODEL_axis_controller_T axis_controller_M_;
RT_MODEL_axis_controller_T *const axis_controller_M = &axis_controller_M_;

/*
 * This function updates continuous states using the ODE3 fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  /* Solver Matrices */
  static const real_T rt_ODE3_A[3] = {
    1.0/2.0, 3.0/4.0, 1.0
  };

  static const real_T rt_ODE3_B[3][3] = {
    { 1.0/2.0, 0.0, 0.0 },

    { 0.0, 3.0/4.0, 0.0 },

    { 2.0/9.0, 1.0/3.0, 4.0/9.0 }
  };

  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE3_IntgData *id = (ODE3_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T hB[3];
  int_T i;
  int_T nXc = 5;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(y, x,
                (uint_T)nXc*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */
  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  axis_controller_derivatives();

  /* f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*)); */
  hB[0] = h * rt_ODE3_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[0]);
  rtsiSetdX(si, f1);
  axis_controller_step();
  axis_controller_derivatives();

  /* f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*)); */
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE3_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[1]);
  rtsiSetdX(si, f2);
  axis_controller_step();
  axis_controller_derivatives();

  /* tnew = t + hA(3);
     ynew = y + f*hB(:,3); */
  for (i = 0; i <= 2; i++) {
    hB[i] = h * rt_ODE3_B[2][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2]);
  }

  rtsiSetT(si, tnew);
  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

/* Model step function */
void axis_controller_step(void)
{
  /* local block i/o variables */
  real_T rtb_c;
  if (rtmIsMajorTimeStep(axis_controller_M)) {
    /* set solver stop time */
    if (!(axis_controller_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&axis_controller_M->solverInfo,
                            ((axis_controller_M->Timing.clockTickH0 + 1) *
        axis_controller_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&axis_controller_M->solverInfo,
                            ((axis_controller_M->Timing.clockTick0 + 1) *
        axis_controller_M->Timing.stepSize0 +
        axis_controller_M->Timing.clockTickH0 *
        axis_controller_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(axis_controller_M)) {
    axis_controller_M->Timing.t[0] = rtsiGetT(&axis_controller_M->solverInfo);
  }

  /* Integrator: '<Root>/i'
   *
   * Regarding '<Root>/i':
   *  Limited Integrator
   */
  if (axis_controller_X.i_CSTATE >= axis_controller_P.v_max ) {
    axis_controller_X.i_CSTATE = axis_controller_P.v_max;
  } else if (axis_controller_X.i_CSTATE <= ((-axis_controller_P.v_max)) ) {
    axis_controller_X.i_CSTATE = ((-axis_controller_P.v_max));
  }

  rtb_c = axis_controller_X.i_CSTATE;

  /* Outport: '<Root>/velocity' */
  axis_controller_Y.velocity = rtb_c;

  /* TransferFcn: '<Root>/p3' incorporates:
   *  Inport: '<Root>/reference'
   */
  axis_controller_B.p3 = 0.0;
  axis_controller_B.p3 += axis_controller_P.p3_C * axis_controller_X.p3_CSTATE;
  axis_controller_B.p3 += axis_controller_P.p3_D * axis_controller_U.reference;

  /* TransferFcn: '<Root>/p2' */
  axis_controller_B.p2 = 0.0;
  axis_controller_B.p2 += axis_controller_P.p2_C * axis_controller_X.p2_CSTATE;
  axis_controller_B.p2 += axis_controller_P.p2_D * axis_controller_B.p3;

  /* TransferFcn: '<Root>/p1' */
  rtb_c = 0.0;
  rtb_c += axis_controller_P.p1_C * axis_controller_X.p1_CSTATE;
  rtb_c += axis_controller_P.p1_D * axis_controller_B.p2;

  /* Sum: '<Root>/Sum7' incorporates:
   *  Inport: '<Root>/pre_pose'
   */
  axis_controller_B.Sum7 = rtb_c - axis_controller_U.pre_pose;

  /* TransferFcn: '<Root>/c' */
  rtb_c = 0.0;
  rtb_c += axis_controller_P.c_C * axis_controller_X.c_CSTATE;
  rtb_c += axis_controller_P.c_D * axis_controller_B.Sum7;

  /* Gain: '<Root>/k_V7' */
  axis_controller_B.k_V7 = axis_controller_P.k_V7_Gain * rtb_c;
  if (rtmIsMajorTimeStep(axis_controller_M)) {
    /* Matfile logging */
    rt_UpdateTXYLogVars(axis_controller_M->rtwLogInfo,
                        (axis_controller_M->Timing.t));
  }                                    /* end MajorTimeStep */

  if (rtmIsMajorTimeStep(axis_controller_M)) {
    /* signal main to stop simulation */
    {                                  /* Sample time: [0.0s, 0.0s] */
      if ((rtmGetTFinal(axis_controller_M)!=-1) &&
          !((rtmGetTFinal(axis_controller_M)-
             (((axis_controller_M->Timing.clockTick1+
                axis_controller_M->Timing.clockTickH1* 4294967296.0)) * 0.001)) >
            (((axis_controller_M->Timing.clockTick1+
               axis_controller_M->Timing.clockTickH1* 4294967296.0)) * 0.001) *
            (DBL_EPSILON))) {
        rtmSetErrorStatus(axis_controller_M, "Simulation finished");
      }
    }

    rt_ertODEUpdateContinuousStates(&axis_controller_M->solverInfo);

    /* Update absolute time for base rate */
    /* The "clockTick0" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick0"
     * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick0 and the high bits
     * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++axis_controller_M->Timing.clockTick0)) {
      ++axis_controller_M->Timing.clockTickH0;
    }

    axis_controller_M->Timing.t[0] = rtsiGetSolverStopTime
      (&axis_controller_M->solverInfo);

    {
      /* Update absolute timer for sample time: [0.001s, 0.0s] */
      /* The "clockTick1" counts the number of times the code of this task has
       * been executed. The resolution of this integer timer is 0.001, which is the step size
       * of the task. Size of "clockTick1" ensures timer will not overflow during the
       * application lifespan selected.
       * Timer of this task consists of two 32 bit unsigned integers.
       * The two integers represent the low bits Timing.clockTick1 and the high bits
       * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
       */
      axis_controller_M->Timing.clockTick1++;
      if (!axis_controller_M->Timing.clockTick1) {
        axis_controller_M->Timing.clockTickH1++;
      }
    }
  }                                    /* end MajorTimeStep */
}

/* Derivatives for root system: '<Root>' */
void axis_controller_derivatives(void)
{
  XDot_axis_controller_T *_rtXdot;
  _rtXdot = ((XDot_axis_controller_T *) axis_controller_M->ModelData.derivs);

  /* Derivatives for Integrator: '<Root>/i' */
  {
    boolean_T lsat;
    boolean_T usat;
    lsat = ( axis_controller_X.i_CSTATE <= ((-axis_controller_P.v_max)) );
    usat = ( axis_controller_X.i_CSTATE >= axis_controller_P.v_max );
    if ((!lsat && !usat) ||
        (lsat && (axis_controller_B.k_V7 > 0)) ||
        (usat && (axis_controller_B.k_V7 < 0)) ) {
      ((XDot_axis_controller_T *) axis_controller_M->ModelData.derivs)->i_CSTATE
        = axis_controller_B.k_V7;
    } else {
      /* in saturation */
      ((XDot_axis_controller_T *) axis_controller_M->ModelData.derivs)->i_CSTATE
        = 0.0;
    }
  }

  /* Derivatives for TransferFcn: '<Root>/p3' incorporates:
   *  Derivatives for Inport: '<Root>/reference'
   */
  _rtXdot->p3_CSTATE = 0.0;
  _rtXdot->p3_CSTATE += axis_controller_P.p3_A * axis_controller_X.p3_CSTATE;
  _rtXdot->p3_CSTATE += axis_controller_U.reference;

  /* Derivatives for TransferFcn: '<Root>/p2' */
  _rtXdot->p2_CSTATE = 0.0;
  _rtXdot->p2_CSTATE += axis_controller_P.p2_A * axis_controller_X.p2_CSTATE;
  _rtXdot->p2_CSTATE += axis_controller_B.p3;

  /* Derivatives for TransferFcn: '<Root>/p1' */
  _rtXdot->p1_CSTATE = 0.0;
  _rtXdot->p1_CSTATE += axis_controller_P.p1_A * axis_controller_X.p1_CSTATE;
  _rtXdot->p1_CSTATE += axis_controller_B.p2;

  /* Derivatives for TransferFcn: '<Root>/c' */
  _rtXdot->c_CSTATE = 0.0;
  _rtXdot->c_CSTATE += axis_controller_P.c_A * axis_controller_X.c_CSTATE;
  _rtXdot->c_CSTATE += axis_controller_B.Sum7;
}

/* Model initialize function */
void axis_controller_initialize(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)axis_controller_M, 0,
                sizeof(RT_MODEL_axis_controller_T));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&axis_controller_M->solverInfo,
                          &axis_controller_M->Timing.simTimeStep);
    rtsiSetTPtr(&axis_controller_M->solverInfo, &rtmGetTPtr(axis_controller_M));
    rtsiSetStepSizePtr(&axis_controller_M->solverInfo,
                       &axis_controller_M->Timing.stepSize0);
    rtsiSetdXPtr(&axis_controller_M->solverInfo,
                 &axis_controller_M->ModelData.derivs);
    rtsiSetContStatesPtr(&axis_controller_M->solverInfo, (real_T **)
                         &axis_controller_M->ModelData.contStates);
    rtsiSetNumContStatesPtr(&axis_controller_M->solverInfo,
      &axis_controller_M->Sizes.numContStates);
    rtsiSetErrorStatusPtr(&axis_controller_M->solverInfo, (&rtmGetErrorStatus
      (axis_controller_M)));
    rtsiSetRTModelPtr(&axis_controller_M->solverInfo, axis_controller_M);
  }

  rtsiSetSimTimeStep(&axis_controller_M->solverInfo, MAJOR_TIME_STEP);
  axis_controller_M->ModelData.intgData.y = axis_controller_M->ModelData.odeY;
  axis_controller_M->ModelData.intgData.f[0] = axis_controller_M->
    ModelData.odeF[0];
  axis_controller_M->ModelData.intgData.f[1] = axis_controller_M->
    ModelData.odeF[1];
  axis_controller_M->ModelData.intgData.f[2] = axis_controller_M->
    ModelData.odeF[2];
  axis_controller_M->ModelData.contStates = ((X_axis_controller_T *)
    &axis_controller_X);
  rtsiSetSolverData(&axis_controller_M->solverInfo, (void *)
                    &axis_controller_M->ModelData.intgData);
  rtsiSetSolverName(&axis_controller_M->solverInfo,"ode3");
  rtmSetTPtr(axis_controller_M, &axis_controller_M->Timing.tArray[0]);
  rtmSetTFinal(axis_controller_M, 10.0);
  axis_controller_M->Timing.stepSize0 = 0.001;

  /* Setup for data logging */
  {
    static RTWLogInfo rt_DataLoggingInfo;
    axis_controller_M->rtwLogInfo = &rt_DataLoggingInfo;
  }

  /* Setup for data logging */
  {
    rtliSetLogXSignalInfo(axis_controller_M->rtwLogInfo, (NULL));
    rtliSetLogXSignalPtrs(axis_controller_M->rtwLogInfo, (NULL));
    rtliSetLogT(axis_controller_M->rtwLogInfo, "tout");
    rtliSetLogX(axis_controller_M->rtwLogInfo, "");
    rtliSetLogXFinal(axis_controller_M->rtwLogInfo, "");
    rtliSetLogVarNameModifier(axis_controller_M->rtwLogInfo, "rt_");
    rtliSetLogFormat(axis_controller_M->rtwLogInfo, 0);
    rtliSetLogMaxRows(axis_controller_M->rtwLogInfo, 1000);
    rtliSetLogDecimation(axis_controller_M->rtwLogInfo, 1);

    /*
     * Set pointers to the data and signal info for each output
     */
    {
      static void * rt_LoggedOutputSignalPtrs[] = {
        &axis_controller_Y.velocity
      };

      rtliSetLogYSignalPtrs(axis_controller_M->rtwLogInfo, ((LogSignalPtrsType)
        rt_LoggedOutputSignalPtrs));
    }

    {
      static int_T rt_LoggedOutputWidths[] = {
        1
      };

      static int_T rt_LoggedOutputNumDimensions[] = {
        1
      };

      static int_T rt_LoggedOutputDimensions[] = {
        1
      };

      static boolean_T rt_LoggedOutputIsVarDims[] = {
        0
      };

      static void* rt_LoggedCurrentSignalDimensions[] = {
        (NULL)
      };

      static int_T rt_LoggedCurrentSignalDimensionsSize[] = {
        4
      };

      static BuiltInDTypeId rt_LoggedOutputDataTypeIds[] = {
        SS_DOUBLE
      };

      static int_T rt_LoggedOutputComplexSignals[] = {
        0
      };

      static const char_T *rt_LoggedOutputLabels[] = {
        "" };

      static const char_T *rt_LoggedOutputBlockNames[] = {
        "axis_controller/velocity" };

      static RTWLogDataTypeConvert rt_RTWLogDataTypeConvert[] = {
        { 0, SS_DOUBLE, SS_DOUBLE, 0, 0, 0, 1.0, 0, 0.0 }
      };

      static RTWLogSignalInfo rt_LoggedOutputSignalInfo[] = {
        {
          1,
          rt_LoggedOutputWidths,
          rt_LoggedOutputNumDimensions,
          rt_LoggedOutputDimensions,
          rt_LoggedOutputIsVarDims,
          rt_LoggedCurrentSignalDimensions,
          rt_LoggedCurrentSignalDimensionsSize,
          rt_LoggedOutputDataTypeIds,
          rt_LoggedOutputComplexSignals,
          (NULL),

          { rt_LoggedOutputLabels },
          (NULL),
          (NULL),
          (NULL),

          { rt_LoggedOutputBlockNames },

          { (NULL) },
          (NULL),
          rt_RTWLogDataTypeConvert
        }
      };

      rtliSetLogYSignalInfo(axis_controller_M->rtwLogInfo,
                            rt_LoggedOutputSignalInfo);

      /* set currSigDims field */
      rt_LoggedCurrentSignalDimensions[0] = &rt_LoggedOutputWidths[0];
    }

    rtliSetLogY(axis_controller_M->rtwLogInfo, "yout");
  }

  /* block I/O */
  (void) memset(((void *) &axis_controller_B), 0,
                sizeof(B_axis_controller_T));

  /* states (continuous) */
  {
    (void) memset((void *)&axis_controller_X, 0,
                  sizeof(X_axis_controller_T));
  }

  /* external inputs */
  (void) memset((void *)&axis_controller_U, 0,
                sizeof(ExtU_axis_controller_T));

  /* external outputs */
  axis_controller_Y.velocity = 0.0;

  /* Matfile logging */
  rt_StartDataLoggingWithStartTime(axis_controller_M->rtwLogInfo, 0.0,
    rtmGetTFinal(axis_controller_M), axis_controller_M->Timing.stepSize0,
    (&rtmGetErrorStatus(axis_controller_M)));

  /* InitializeConditions for Integrator: '<Root>/i' */
  axis_controller_X.i_CSTATE = axis_controller_P.i_IC;

  /* InitializeConditions for TransferFcn: '<Root>/p3' */
  axis_controller_X.p3_CSTATE = 0.0;

  /* InitializeConditions for TransferFcn: '<Root>/p2' */
  axis_controller_X.p2_CSTATE = 0.0;

  /* InitializeConditions for TransferFcn: '<Root>/p1' */
  axis_controller_X.p1_CSTATE = 0.0;

  /* InitializeConditions for TransferFcn: '<Root>/c' */
  axis_controller_X.c_CSTATE = 0.0;
}

/* Model terminate function */
void axis_controller_terminate(void)
{
  /* (no terminate code required) */
}
