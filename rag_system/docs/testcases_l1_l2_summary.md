# L1/L2 Test Case Summary (from logs/trace.jsonl)

Source: `logs/trace.jsonl`

## L1 Test Cases (eval_l1)
1. What is the current API rate limit for PaymentGW?
   - 2026-05-08 09:27:31.159926 (session: eval_l1)
2. Who leads Team Platform and what services do they own?
   - 2026-05-08 09:27:34.254109 (session: eval_l1)
3. What was the root cause of the March 5, 2026 PaymentGW outage?
   - 2026-05-08 09:27:38.784975 (session: eval_l1)
4. What is GeekBrain's data retention policy for transaction logs?
   - 2026-05-08 09:27:41.652604 (session: eval_l1)
5. What are GeekBrain's production deployment windows?
   - 2026-05-08 09:27:45.925364 (session: eval_l1)
6. What authentication method does the PaymentGW API use?
   - 2026-05-08 09:27:49.639489 (session: eval_l1)
7. What message queue does NotificationSvc use?
   - 2026-05-08 09:27:52.713191 (session: eval_l1)
8. After the March 5 PaymentGW incident, a circuit breaker review was scheduled. What was the deadline?
   - 2026-05-08 09:27:55.986991 (session: eval_l1)
9. What programming language is AuthSvc written in?
   - 2026-05-08 09:27:58.754607 (session: eval_l1)
10. How often does GeekBrain rotate JWT signing keys?
   - 2026-05-08 09:28:02.030017 (session: eval_l1)

## L2 Test Cases (all runs)
1. What is PaymentGW's API rate limit?
   - 2026-05-08 09:28:04.794128 (eval_l2)
   - 2026-05-08 09:41:35.594027 (eval_l2_fix)
   - 2026-05-08 09:58:45.244875 (eval_l2_final)
   - 2026-05-08 10:18:46.350915 (eval_l2_final2)
   - 2026-05-08 10:40:29.341784 (eval_l2_run)
   - 2026-05-08 11:09:23.505334 (eval_l2_run2)
   - 2026-05-08 11:22:55.347157 (eval_l2_dbg)
   - 2026-05-08 11:56:13.286100 (eval_l2_run3)
2. If Team Commerce discovers a P1 bug in OrderSvc at 21:00 on a Friday, can they deploy a fix? What is the process?
   - 2026-05-08 09:28:10.336859 (eval_l2)
   - 2026-05-08 09:41:42.057727 (eval_l2_fix)
   - 2026-05-08 09:58:58.349625 (eval_l2_final)
   - 2026-05-08 10:18:51.945319 (eval_l2_final2)
   - 2026-05-08 10:40:34.970761 (eval_l2_run)
   - 2026-05-08 11:09:29.235734 (eval_l2_run2)
   - 2026-05-08 11:56:19.475299 (eval_l2_run3)
3. Which services would be directly affected if AuthSvc goes completely down?
   - 2026-05-08 09:28:14.535799 (eval_l2)
   - 2026-05-08 09:41:45.442406 (eval_l2_fix)
   - 2026-05-08 09:59:02.045243 (eval_l2_final)
   - 2026-05-08 10:18:56.463521 (eval_l2_final2)
   - 2026-05-08 10:40:39.074995 (eval_l2_run)
   - 2026-05-08 11:09:31.936339 (eval_l2_run2)
   - 2026-05-08 11:56:22.117311 (eval_l2_run3)
4. Based on the Q1 review and the cost optimization initiative, which services are the top priorities for cost reduction and why?
   - 2026-05-08 09:28:21.385137 (eval_l2)
   - 2026-05-08 09:41:53.528801 (eval_l2_fix)
   - 2026-05-08 09:59:15.760308 (eval_l2_final)
   - 2026-05-08 10:19:02.299081 (eval_l2_final2)
   - 2026-05-08 10:40:44.595882 (eval_l2_run)
   - 2026-05-08 11:09:36.228750 (eval_l2_run2)
   - 2026-05-08 11:23:01.311802 (eval_l2_dbg)
   - 2026-05-08 11:56:25.970382 (eval_l2_run3)
5. What common lessons emerged from the March 2026 incidents at PaymentGW and FraudDetector?
   - 2026-05-08 09:28:27.663665 (eval_l2)
   - 2026-05-08 09:42:01.002472 (eval_l2_fix)
   - 2026-05-08 09:59:22.134216 (eval_l2_final)
   - 2026-05-08 10:19:09.797907 (eval_l2_final2)
   - 2026-05-08 10:40:50.970373 (eval_l2_run)
   - 2026-05-08 11:09:41.658268 (eval_l2_run2)
   - 2026-05-08 11:56:31.742184 (eval_l2_run3)
6. What should a new engineer joining Team Data know about the systems they'll work with, based on the onboarding guide and team information?
   - 2026-05-08 09:28:35.311303 (eval_l2)
   - 2026-05-08 09:42:13.087443 (eval_l2_fix)
   - 2026-05-08 09:59:28.965833 (eval_l2_final)
   - 2026-05-08 10:19:16.134906 (eval_l2_final2)
   - 2026-05-08 10:40:57.937394 (eval_l2_run)
   - 2026-05-08 11:09:48.416804 (eval_l2_run2)
   - 2026-05-08 11:23:06.680316 (eval_l2_dbg)
   - 2026-05-08 11:56:38.192133 (eval_l2_run3)
7. The Q1 2026 review mentioned concerns about NotificationSvc. What specific issues were raised, and what does the capacity planning document propose to fix them?
   - 2026-05-08 09:28:41.249237 (eval_l2)
   - 2026-05-08 09:42:21.686720 (eval_l2_fix)
   - 2026-05-08 09:59:35.521399 (eval_l2_final)
   - 2026-05-08 10:19:21.641167 (eval_l2_final2)
   - 2026-05-08 10:41:04.385851 (eval_l2_run)
   - 2026-05-08 11:09:54.397034 (eval_l2_run2)
   - 2026-05-08 11:56:43.722692 (eval_l2_run3)
8. What is the complete escalation path for a P1 incident on PaymentGW, from detection to CTO notification? Include specific names and timeframes.
   - 2026-05-08 09:28:45.653374 (eval_l2)
   - 2026-05-08 09:42:27.936482 (eval_l2_fix)
   - 2026-05-08 09:59:39.309351 (eval_l2_final)
   - 2026-05-08 10:19:27.281260 (eval_l2_final2)
   - 2026-05-08 10:41:08.993447 (eval_l2_run)
   - 2026-05-08 11:10:02.337442 (eval_l2_run2)
   - 2026-05-08 11:23:10.622204 (eval_l2_dbg)
   - 2026-05-08 11:56:48.535023 (eval_l2_run3)
