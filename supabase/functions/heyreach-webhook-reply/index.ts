import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

const SLACK_WEBHOOKS = [
  Deno.env.get("SLACK_WEBHOOK_URL"),
  Deno.env.get("SLACK_WEBHOOK_URL2"),
].filter(Boolean) as string[];

async function sendSlack(leadName: string | null, campaignName: string | null, leadLinkedin: string | null, messageText: string | null) {
  const blocks = [
    {
      type: "header",
      text: { type: "plain_text", text: ":speech_balloon: Investor Reply Received!", emoji: true },
    },
    {
      type: "section",
      fields: [
        { type: "mrkdwn", text: `*Lead:*\n${leadName || "Unknown"}` },
        { type: "mrkdwn", text: `*Campaign:*\n${campaignName || "Unknown"}` },
      ],
    },
    ...(messageText
      ? [{ type: "section", text: { type: "mrkdwn", text: `*Message:*\n>${messageText.substring(0, 300)}${messageText.length > 300 ? "..." : ""}` } }]
      : []),
    ...(leadLinkedin
      ? [{ type: "section", text: { type: "mrkdwn", text: `*LinkedIn:* <${leadLinkedin}|View Profile>` } }]
      : []),
    {
      type: "context",
      elements: [{ type: "mrkdwn", text: `NextStep Investor Outreach | ${new Date().toISOString().slice(0, 16).replace("T", " ")} UTC` }],
    },
  ];

  for (const url of SLACK_WEBHOOKS) {
    try {
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ blocks }),
      });
    } catch (_) {}
  }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const body = await req.json();

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    const eventType = body.eventType || body.event_type || body.type || "MESSAGE_REPLY_RECEIVED";
    const leadName = body.leadName || body.lead_name || null;
    const leadLinkedin = body.leadLinkedInUrl || body.profileUrl || null;
    const campaignName = body.campaignName || body.campaign_name || null;
    const messageText = body.messageText || body.message || null;

    const { error } = await supabase.from("heyreach_events").insert({
      event_type: eventType,
      lead_name: leadName,
      lead_linkedin: leadLinkedin,
      campaign_name: campaignName,
      campaign_id: body.campaignId || body.campaign_id || null,
      message_text: messageText,
      raw_payload: body,
    });

    if (error) throw error;

    await sendSlack(leadName, campaignName, leadLinkedin, messageText);

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
