// Rules checked by the gateway BEFORE any tool runs.
// Default deny: anything not permitted here is refused.

// Anyone may look up an order.
permit(
  principal,
  action == Action::"refund-api___getOrder",
  resource
);

// Refunds are allowed only below 1000.
permit(
  principal,
  action == Action::"refund-api___processRefund",
  resource
) when { context.input.amount < 1000 };
