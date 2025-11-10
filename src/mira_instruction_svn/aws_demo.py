from instruction import Instruction
from sequence import Sequence

# Shared Audit Step
log_audit = Instruction("secure data read", "CloudTrail Log", "audit complete")

# Trusted Path (would run if internal IP; here, fails for external)
trusted_condition = Instruction("request IP in trusted range", "Evaluate Condition", "access allowed")
trusted_allow = Instruction("access allowed", "Allow GetObject", "secure data read")

seq_trusted = Sequence([trusted_condition, trusted_allow, log_audit])

# Set intention (secure analytics)
for instr in seq_trusted.instructions:
    instr.set_intention(True)

# Simulate External IP: Trusted path fails entirely
trusted_condition.mark_executed(False)  # False: IP not in range
trusted_allow.mark_executed(False)      # No execution
log_audit.mark_executed(False)          # No logging (chain broken)

print("=== TRUSTED PATH (Fails for External IP) ===")
order_trusted = seq_trusted.arthakrama_order("audit complete")
for i in order_trusted or []:
    print(f"{i} → {i.evaluate()}")  # V for all (intent violated by failure)

# External/Deny Path (runs for external IP)
external_condition = Instruction("request IP external", "Evaluate Condition", "access denied")
deny_access = Instruction("access denied", "Implicit Deny GetObject", "access blocked")
alert_log = Instruction("access blocked", "GuardDuty Alert", "violation audited")

seq_external = Sequence([external_condition, deny_access, alert_log])

# Set intention
for instr in seq_external.instructions:
    instr.set_intention(True)

# Simulate: External path succeeds (Deny triggered)
external_condition.mark_executed(True)   # True: IP external → condition for Deny holds
deny_access.mark_executed(True)          # Deny succeeds
alert_log.mark_executed(True)            # Alert succeeds

print("\n=== EXTERNAL PATH (Succeeds: Deny + Alert) ===")
order_external = seq_external.arthakrama_order("violation audited")
for i in order_external:
    print(f"{i} → {i.evaluate()}")  # S for all (Deny goal achieved)

# Overall Intent: Secure access violated (V)
print("\n=== OVERALL INTENT (Secure Analytics) ===")
print("Trusted Path: V (access blocked, intent unmet)")
print("External Path: S (Deny succeeded), but high-level V (no secure read)")